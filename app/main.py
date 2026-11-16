from pathlib import Path

from ingestion.pipeline import init_pipeline
from chunking import create_chunks
from embeddings import create_embeddings, get_openai_client
from vectorstore.pipeline import initialize_vector_store_pipeline, get_index
from generation.pipeline import query_response_pipeline


def run_ingestion():
    pdf_dir = Path(__file__).parent.parent / "data"
    print("Ingestion in process.....")

    sentences = init_pipeline(pdf_dir)
    print("Loaded PDF.....")
    chunked_documents = create_chunks(sentences)
    print("Chunked Sentences.....")
    _, embeddings = create_embeddings(chunked_documents)
    print("Created Embeddings.....")
    initialize_vector_store_pipeline(embeddings)
    print("Stored Embeddings.....")


def main():
    should_ingest = input(
        "Do you want to ingest and write new embeddings to the vector db? (yes/no): "
    )
    if should_ingest.strip().lower() == "yes":
        run_ingestion()

    client = get_openai_client()
    index = get_index()
    print("Connected to vector store.....")

    while True:
        question = input("Ask your question or type 'end' to end the prompts: ")
        print()

        if question == "end":
            print("Bye Bye")
            break

        output = query_response_pipeline(client, index, question)
        print(output)
        print()


if __name__ == "__main__":
    main()