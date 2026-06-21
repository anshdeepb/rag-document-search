from vectorstore.pinecone_client import initialize_db
from vectorstore.vector_builder import create_vectors
from vectorstore.upsert import upsert_vectors_to_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

def initialize_vector_store_pipeline(embeddings, boolean):
    index = initialize_db(api_key)
    vectors = create_vectors(embeddings)
    upsert_vectors_to_vector_store(index, vectors, boolean)

    return index

