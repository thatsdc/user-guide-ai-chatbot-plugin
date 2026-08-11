import pytest
from unittest.mock import patch
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval import assert_test
from test_cases import ANSWER_RELEVANCY_TEST_CASES
from utils import execute_test_agent, create_mock_tools, JUDGE_MODEL
from eval_tracker import tracker

from unittest.mock import patch
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval
from deepeval import assert_test

jenkins_relevancy_metric = GEval(
    name="Jenkins Answer Relevancy",
    criteria=(
        "Evaluate if the actual_output is a relevant, direct, and helpful response to the input. "
        "CRITICAL SYSTEM RULE: The agent is a strict Jenkins CI/CD troubleshooting assistant. "
        "If the input is unrelated to Jenkins, CI/CD, DevOps, or programming (e.g., cooking recipes, general chatting), "
        "a polite refusal to answer is the ONLY correct and highly relevant response, and MUST receive a score of 1.0. "
        "If the input is related to Jenkins, the answer must directly address the question without unnecessary digressions."
    ),
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    model=JUDGE_MODEL,
    threshold=0.7,
    strict_mode=False,
)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_case", ANSWER_RELEVANCY_TEST_CASES)
@patch("agent.agent.get_tool_list")
async def test_answer_relevancy(mock_get_tool_list, test_case: dict):
    """
    Evaluates Answer Relevancy across multiple scenarios.
    All tools are passed to the agent, but only the targeted ones return useful dummy data.
    """
    dummy_data = test_case["dummy_context"]
    mock_get_tool_list.return_value = create_mock_tools(dummy_data)

    user_prompt = test_case["question"]
    print(f"\n[Testing Prompt]: {user_prompt}")

    # Execute the agent
    actual_output, _ = await execute_test_agent(user_prompt)
    print(f"[Agent Output]: {actual_output}")

    # Define the DeepEval Test Case (No retrieval_context needed for Relevancy)
    test_case_obj = LLMTestCase(
        input=user_prompt,
        actual_output=actual_output,
    )

    # Assert with the metric
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=JUDGE_MODEL)
    try:
        assert_test(test_case_obj, [relevancy_metric])
    finally:
        if relevancy_metric.score:
            tracker.add_score("answer_relevancy", relevancy_metric.score)
