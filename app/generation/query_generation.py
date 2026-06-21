from openai import OpenAI
from generation.query_modelling import model_query

def query_vector_store(client, index, question):
    question = question

    modelled_query = model_query(question)

    response = client.embeddings.create(
    model="text-embedding-3-small",
    input=modelled_query
)

    query_vector = response.data[0].embedding

    query_response = index.query(
    vector=query_vector,
    top_k=100,
    include_metadata=True
)

    query_response_dict = query_response.to_dict()

    return modelled_query, query_response_dict

