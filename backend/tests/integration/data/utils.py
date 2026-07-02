import pytest
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from qdrant_client.http.models import Distance, VectorParams
from typing import List

COLLECTION_NAME = "test_collection"
VECTOR_SIZE = 384


class MockEmbeddingModel(Embeddings):
    """
    Mock embedding model to generate deterministic vectors for testing purposes.
    Matches the required vector size for Qdrant without using real models.
    """

    def __init__(self, vector_dimension: int):
        self.vector_dimension = vector_dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Return a list of fake embeddings matching the configured dimension
        return [[0.1] * self.vector_dimension for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        # Return a single fake embedding for query operations
        return [0.1] * self.vector_dimension


@pytest.fixture(scope="module")
def ephemeral_vector_db():
    client = QdrantClient(":memory:")

    test_embedding_model = MockEmbeddingModel(vector_dimension=VECTOR_SIZE)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

    temporary_db = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=test_embedding_model,
    )

    yield temporary_db

    client.delete_collection(COLLECTION_NAME)
