from openai import OpenAI
import os

def model_query(question):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = f"""
    You are a retrieval query generator for a RAG system.

    Your job:
    Convert the user question into multiple high-quality search queries that would help retrieve relevant documents from a technical knowledge base about algorithms.

    Rules:
    - Do NOT answer the question
    - Do NOT explain anything
    - Output ONLY a JSON object
    - Generate 3–6 queries maximum
    - Make queries diverse (definitions, comparisons, use cases, tradeoffs)
    - Prefer keyword-rich search-style phrases

    User question:
    {question}

    Output format:
    {{
    "queries": [
        "query 1",
        "query 2",
        "query 3"
    ]
    }}
    """

    ai_response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    output = ai_response.output_text
    return output