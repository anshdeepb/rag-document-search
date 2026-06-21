from openai import OpenAI

def query_vector_store(client, index, question):
    question = question

    response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

    query_vector = response.data[0].embedding

    query_response = index.query(
    vector=query_vector,
    top_k=100,
    include_metadata=True
)

    query_response_dict = query_response.to_dict()

    return query_response_dict

