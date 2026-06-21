from openai import OpenAI
import os

def generate_llm_response(prompt):
    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

    ai_response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    temperature=0.5
)

    output = ai_response.output_text
    return output