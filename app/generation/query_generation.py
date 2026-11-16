from openai import OpenAI
from generation.query_modelling import model_query

TOP_K_PER_QUERY = 30

def query_vector_store(client, index, question):
    queries = model_query(question)

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=queries
    )

    matches_by_id = {}
    for item in response.data:
        result = index.query(
            vector=item.embedding,
            top_k=TOP_K_PER_QUERY,
            include_metadata=True
        ).to_dict()

        for match in result["matches"]:
            existing = matches_by_id.get(match["id"])
            if existing is None or match["score"] > existing["score"]:
                matches_by_id[match["id"]] = match

    return queries, {"matches": list(matches_by_id.values())}