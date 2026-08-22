from vectordb.qdrant import get_vector_store
from langchain_core.documents import Document
from qdrant_client import models
import asyncio


async def hybrid_retriever(
    query: str, payload_filter: models.Filter | None = None, k: int = 2
) -> list[Document]:
    """
    Make a query using Qdrant Hybrid Retriever

    Args:
        query (str)
        metadata (dict): Filter using metadata
        k (int): Get top k results

    Returns:
        list[Document]
    """
    try:
        return await get_vector_store().asimilarity_search(
            query=query, k=k, filter=payload_filter
        )
    except Exception as e:
        print("VectorDB Error: ", e)
        return []


if __name__ == "__main__":
    query = "Jenkins EC2 memory"
    results = asyncio.run(hybrid_retriever(query))
    print(results)
