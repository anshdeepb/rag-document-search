def upsert_vectors_to_vector_store(index, vectors):
    BATCH_SIZE = 100

    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i + BATCH_SIZE]
        index.upsert(vectors=batch)
