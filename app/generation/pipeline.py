from generation.query_generation import query_vector_store
from generation.rerank import rerank_results
from generation.context_generation import generate_context
from generation.llm_response_generator import generate_llm_response

def query_response_pipeline(client, index, question):
    modelled_query, query_response_dict = query_vector_store(client, index, question)
    results, documents_to_rerank = rerank_results(modelled_query, query_response_dict)
    prompt = generate_context(modelled_query, results, documents_to_rerank)
    output = generate_llm_response(prompt)

    return output
