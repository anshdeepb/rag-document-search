def generate_context(question, chunks):
    context_blocks = []

    for chunk in chunks:
        if chunk["relevance_score"] < 0.30:
            continue

        context_blocks.append(
            f"--- {chunk['source']}, page {chunk['page']} ---\n{chunk['text']}\n"
        )

    context = "\n".join(context_blocks)

    prompt = f"""
        You are a helpful assistant answering questions using the provided context.

        Rules:
        - Use the context as your PRIMARY source of truth
        - If the context is partially relevant, use what is available and clearly state limitations
        - If the context is missing some details, you may still reason carefully from what is provided
        - Only say "I don't know based on the provided documents" if the context is completely unrelated
        - Cite the page for each claim, e.g. (p. 359)

        Context:
        {context}

        Question:
        {question}

        Answer clearly and concisely:
        """

    return prompt
