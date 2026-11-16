from openai import OpenAI
import os
import json

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
    - Generate 2–5 queries
    - Cover different phrasings of what the user actually asked
    - Only include comparisons or tradeoffs if the question asks for them
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

    output = ai_response.output_text.strip()

    # Models sometimes wrap JSON in ```json ... ``` fences
    if output.startswith("```"):
        output = output.strip("`")
        output = output.removeprefix("json").strip()

    try:
        queries = json.loads(output)["queries"]
    except (json.JSONDecodeError, KeyError, TypeError):
        queries = []

    # Always search with the original question too, and drop duplicates
    all_queries = [question] + [q for q in queries if isinstance(q, str)]
    return list(dict.fromkeys(all_queries))