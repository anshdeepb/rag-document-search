def upsert_vectors_to_vector_store(index, vectors, boolean):
    BATCH_SIZE = 100

    if boolean:
        for i in range(0, len(vectors), BATCH_SIZE):
            batch = vectors[i:i + BATCH_SIZE]
            index.upsert(vectors=batch)
