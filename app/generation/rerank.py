import cohere
from dotenv import load_dotenv
import os

load_dotenv()

def rerank_results(question, query_response_dict):
    documents_to_rerank = [match["metadata"]["text"] for match in query_response_dict["matches"]]

    co = cohere.ClientV2(
        api_key=os.getenv("COHERE_API_KEY")
    )

    results = co.rerank(
        model="rerank-v3.5",
        query=question,
        documents=documents_to_rerank,
        top_n=10
    )   
    
    return results, documents_to_rerank

