import os
from pathlib import Path

import cohere
from dotenv import load_dotenv

load_dotenv()


def rerank_results(question, query_response_dict, top_n=10):
    matches = query_response_dict["matches"]
    if not matches:
        return []

    documents = [match["metadata"]["text"] for match in matches]

    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

    results = co.rerank(
        model="rerank-v3.5",
        query=question,
        documents=documents,
        top_n=min(top_n, len(documents))
    )

    chunks = []
    for result in results.results:
        metadata = matches[result.index]["metadata"]
        chunks.append({
            "text": metadata["text"],
            "source": Path(metadata["source"]).name,
            "page": int(metadata["page"]) + 1,
            "chunk_id": metadata["chunk"],
            "relevance_score": round(result.relevance_score, 3),
        })

    return chunks