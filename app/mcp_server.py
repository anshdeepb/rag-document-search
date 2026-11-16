from mcp.server import MCPServer
from generation.pipeline import retrieve_chunks
import logging
import sys
from functools import lru_cache

from embeddings import get_openai_client
from vectorstore.pipeline import get_index

mcp = MCPServer("rag-document-search")

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("rag-mcp")


@lru_cache(maxsize=1)
def get_resources():
    """Connect once on first use, then reuse for every tool call."""
    logger.info("Connecting to OpenAI and Pinecone...")
    return get_openai_client(), get_index()


@mcp.tool()
def search_documents(query: str, top_n: int = 5) -> list[dict]:
    """Search an algorithms textbook (Cormen, Introduction to Algorithms) and return the most relevant passages.

    Use this for questions about algorithms, data structures, complexity, or proofs. Each result includes the passage text, source file,
    PDF page number, and a relevance score (0-1). Cite pages when
    answering from these results.

    Args:
        query: A natural-language question or search phrase.
        top_n: Number of passages to return (1-10).
    """
    top_n = max(1, min(top_n, 10))
    client, index = get_resources()
    return retrieve_chunks(client, index, query, top_n=top_n)

if __name__ == "__main__":
    mcp.run(transport="stdio")