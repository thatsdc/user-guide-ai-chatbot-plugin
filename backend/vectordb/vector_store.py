from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from dotenv import load_dotenv
from manage_env import get_env
import os, base64

load_dotenv()


def get_vector_store():
    HUGGING_FACE_EMBEDDING_NAME = get_env("HUGGING_FACE_EMBEDDING_NAME")
    CHROMA_HOST = get_env("CHROMA_HOST")
    CHROMA_PORT = int(get_env("CHROMA_PORT"))
    CHROMA_SSL = get_env("CHROMA_SSL").lower() == "true"

    CHROMA_TOKEN = os.environ.get("CHROMA_TOKEN", "")

    security_headers = {}
    if CHROMA_TOKEN:
        security_headers = {"Authorization": f"Bearer {CHROMA_TOKEN}"}
    embedding_model = HuggingFaceEmbeddings(model_name=HUGGING_FACE_EMBEDDING_NAME)

    chroma_client = chromadb.HttpClient(
        host=CHROMA_HOST, port=CHROMA_PORT, ssl=CHROMA_SSL, headers=security_headers
    )

    vector_store_server = Chroma(
        client=chroma_client,
        collection_name="production_docs",
        embedding_function=embedding_model,
    )

    return vector_store_server


if __name__ == "__main__":
    vector_store = get_vector_store()
    result = vector_store.similarity_search("jenkins", k=1)
    print(result)
