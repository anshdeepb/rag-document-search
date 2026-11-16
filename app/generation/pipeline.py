from generation.query_generation import query_vector_store
from generation.rerank import rerank_results
from generation.context_generation import generate_context
from generation.llm_response_generator import generate_llm_response


def retrieve_chunks(client, index, question, top_n=10):
    """Rewrite → search → rerank. No answer generation."""
    _, query_response_dict = query_vector_store(client, index, question)
    return rerank_results(question, query_response_dict, top_n)


def query_response_pipeline(client, index, question):
    chunks = retrieve_chunks(client, index, question)
    prompt = generate_context(question, chunks)
    return generate_llm_response(prompt)