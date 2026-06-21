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
        You are a helpful assistant answering questions using the provided context.

        Rules:
        - Use the context as your PRIMARY source of truth
        - If the context is partially relevant, use what is available and clearly state limitations
        - If the context is missing some details, you may still reason carefully from what is provided
        - Only say "I don't know based on the provided documents" if the context is completely unrelated

        Context:
        {context}

        Question:
        {question}

        Answer clearly and concisely:
        """

    return prompt
