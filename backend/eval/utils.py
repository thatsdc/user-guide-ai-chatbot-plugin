from langchain_core.tools import tool
from manage_env import get_env
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState
from agent.agent import Agent
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_core.language_models.chat_models import BaseChatModel
from llm_client import get_llm_client
import pytest


class CustomLangChainJudge(DeepEvalBaseLLM):
    """
    A custom wrapper that bridges DeepEval with any LangChain BaseChatModel.
    """

    def __init__(
        self, provider: str, model_name: str, api_key: str = "", base_url: str = ""
    ):
        self.provider = provider
        self.model_name = model_name

        self.chat_model: BaseChatModel = get_llm_client(
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.0,
        )

    def load_model(self) -> "CustomLangChainJudge":
        """
        Satisfies the DeepEvalBaseLLM interface requirement.
        Must return the DeepEval model instance itself.
        """
        return self

    def generate(self, prompt: str) -> str:
        """Synchronous text generation for DeepEval."""
        response = self.chat_model.invoke(prompt)
        return str(response.content)

    async def a_generate(self, prompt: str) -> str:
        """Asynchronous text generation for DeepEval parallel execution."""
        response = await self.chat_model.ainvoke(prompt)
        return str(response.content)

    def get_model_name(self) -> str:
        """Returns the identifier of the model for reports."""
        return f"{self.provider}:{self.model_name}"


JUDGE_LLM_PROVIDER = get_env("JUDGE_LLM_PROVIDER")
JUDGE_LLM_MODEL_NAME = get_env("JUDGE_LLM_MODEL_NAME")
JUDGE_LLM_BASE_URL = get_env("JUDGE_LLM_BASE_URL")
JUDGE_LLM_API_KEY = get_env("JUDGE_LLM_API_KEY")

if not JUDGE_LLM_PROVIDER or not JUDGE_LLM_MODEL_NAME:
    pytest.skip(
        "JUDGE_LLM_PROVIDER and JUDGE_LLM_MODEL_NAME must be set to run eval tests.",
        allow_module_level=True,
    )

JUDGE_MODEL = CustomLangChainJudge(
    provider=JUDGE_LLM_PROVIDER,
    model_name=JUDGE_LLM_MODEL_NAME,
    api_key=JUDGE_LLM_API_KEY,
    base_url=JUDGE_LLM_BASE_URL,
)

LANGFUSE_TRACING = get_env("LANGFUSE_TRACING").upper() == "TRUE"
LANGSMITH_TRACING = get_env("LANGSMITH_TRACING").upper() == "TRUE"


async def execute_test_agent(prompt: str, chat_id: int = 999) -> tuple[str, list[str]]:
    """
    Instantiates and runs the LangGraph agent in memory.
    Returns the final actual_output AND the retrieval_context (data returned by tools).
    """

    agent_instance = Agent(
        chat_id=chat_id,
        prompt=prompt,
        context={},
        checkpointer=MemorySaver(),  # type: ignore
    )

    app = agent_instance.create_state_graph()
    input_state: MessagesState = {"messages": [HumanMessage(content=prompt)]}

    callbacks: list = []
    metadata = {}
    langfuse_handler = None
    if LANGFUSE_TRACING:
        from langfuse.langchain import CallbackHandler

        langfuse_handler = CallbackHandler()
        callbacks.append(langfuse_handler)
        metadata.update(
            {"langfuse_session_id": str(chat_id), "langfuse_tags": ["eval"]}
        )

    if LANGSMITH_TRACING:
        metadata.update(
            {
                "environment": "eval",
            }
        )

    execution_config: RunnableConfig = {
        "configurable": {"thread_id": str(chat_id)},
        "callbacks": callbacks,
        "metadata": metadata,
    }

    final_state = await app.ainvoke(input_state, config=execution_config)

    actual_output = ""
    retrieval_context = []

    for msg in final_state["messages"]:
        # Extract the final answer: AIMessage without tool calls
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            actual_output = str(msg.content)

        # Extract the context: Output from the mocked tools
        elif isinstance(msg, ToolMessage):
            retrieval_context.append(str(msg.content))

    return actual_output, retrieval_context


def create_mock_tools(dummy_context_data: dict) -> list:
    """
    Dynamically generates the full list of tools for the agent.
    Returns the specific dummy data injected via the test case, or a fallback empty string/JSON.
    """

    @tool
    async def fetch_from_vectordb(query: str) -> str:
        """
        Query the vector database for official documentation and community Q&A.
        Use this tool ONLY for Jenkins concepts.
        Do NOT use this tool to search for specific build logs, information regarding the job details, or user local context.

        Args:
            query: The search input (e.g., "How to write a declarative pipeline", "Docker plugin setup").
        """
        return dummy_context_data.get("fetch_from_vectordb", "No documentation found.")

    @tool
    async def get_general_jenkins_context() -> str:
        """
        Retrieve global settings for the current user's Jenkins instance.
        Use this tool to find out the Jenkins version, the master configuration,
        system messages, and the current screen the user is viewing.
        """
        return dummy_context_data.get("get_general_jenkins_context", "{}")

    @tool
    async def get_installed_plugin_list() -> str:
        """
        Retrieve the complete list of plugins currently installed on the user's Jenkins instance.
        Use this tool to verify if a specific plugin is available or to check plugin versions
        before suggesting a solution that requires them.
        """
        return dummy_context_data.get("get_installed_plugin_list", "{}")

    @tool
    async def get_job_details() -> str:
        """
        Retrieve the configuration details of the specific Jenkins Job/Pipeline the user is currently looking at.
        Use this tool to inspect the pipeline definition, repository URLs, and config.xml.
        Do NOT use this tool to find execution logs (use get_build_details instead).
        """
        return dummy_context_data.get("get_job_details", "{}")

    @tool
    async def get_build_details(log_search_query: str) -> str:
        """
        Retrieve the execution details of the current Jenkins build (status, timestamp, duration) the user is currently looking at
        AND search its console logs for specific errors or keywords.

        Args:
            log_search_query: A specific keyword or error type to search within the build logs
                                (e.g., "Exception", "NullPointer", "npm ERR!", "timeout").
                                If you need to search for errors you can pass "error".
        """
        return dummy_context_data.get("get_build_details", "{}")

    @tool
    async def get_workspace_tree() -> str:
        """
        Retrieves the directory tree of ALL workspaces associated with the current build.
        Use this to explore available files before reading their content.

        Args:
            query: Ignored, but required by the framework.
            chat_id: The ID of the current chat.
        """
        return dummy_context_data.get("get_workspace_tree", "")

    @tool
    async def get_workspace_file(file_path: str, workspace_id: str) -> str:
        """
        Reads the content of a specific file within a Jenkins workspace.
        Do NOT call this tool until you have called get_workspace_tree().
        You MUST call get_workspace_tree() tool first to obtain the correct 'workspace_id' and exact 'file_path'.

        Args:
            file_path: The relative path of the file (e.g., 'src/main/java/App.java' or 'pom.xml')
            workspace_id: The workspace ID provided by get_workspace_tree() (e.g., 'ws-default' or 'ws-pipeline-1')
            chat_id: The ID of the current chat.
        """
        return dummy_context_data.get("get_workspace_file", "File not found.")

    return [
        fetch_from_vectordb,
        get_general_jenkins_context,
        get_installed_plugin_list,
        get_job_details,
        get_build_details,
        get_workspace_tree,
        get_workspace_file,
    ]
