def create_vectors(embeddings):
    vectors = []

    for embedding in embeddings:
        unique_id = f"{embedding['source']}_{embedding['page']}_{embedding['chunk_id']}"

        vectors.append({
        "id": str(unique_id),
        # FIX 2: Removed .tolist() because OpenAI outputs native lists directly
        "values": embedding["embedding"], 
        "metadata": {
            "page": embedding["page"],
            "source": embedding["source"],
            "chunk": embedding["chunk_id"],
            "text": embedding["text"]
        }
    })
        
    return vectors
