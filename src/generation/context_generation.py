def generate_context(question, results, documents_to_rerank):
    context_blocks = []

    for result in results.results:
        original_index = result.index
        relevance_score = result.relevance_score

        if relevance_score < 0.30:
            continue

        matching_text = documents_to_rerank[original_index]
        context_blocks.append(f"--- Document Chunk ---\n{matching_text}\n")

    context = "\n".join(context_blocks)

    prompt = f"""
        You are a helpful assistant. Use ONLY the context below to answer the question.
        If the answer is not in the context, say "I don't know based on the provided documents."
        Context:
        {context}
        Question:
        {question}
        Answer:
        """

    return prompt
