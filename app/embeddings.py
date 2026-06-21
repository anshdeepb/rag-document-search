import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

def create_embeddings(chunked_documents):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    texts_to_embed = [chunk["text"] for chunk in chunked_documents]

    BATCH_SIZE = 500
    all_vectors = []

    for i in range(0, len(texts_to_embed), BATCH_SIZE):
        batch = texts_to_embed[i : i + BATCH_SIZE]
    
    # Request embeddings just for this specific batch
        response = client.embeddings.create(
        model="text-embedding-3-small",
        input=batch
    )
    
    # Extract vectors and add them to our master list
        for data_object in response.data:
            all_vectors.append(data_object.embedding)

    embeddings = []

    for i, chunked_doc in enumerate(chunked_documents):
        embeddings.append({
        "embedding" : all_vectors[i],
        "text" : chunked_doc["text"],
        "source" : chunked_doc["source"],
        "page" : chunked_doc["page"],
        "chunk_id" : chunked_doc["chunk_id"]
    })

    return client, embeddings