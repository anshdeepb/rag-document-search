from pathlib import Path

from ingestion.pipeline import init_pipeline
from chunking import create_chunks
from embeddings import create_embeddings
from vectorstore.pipeline import initialize_vector_store_pipeline
from generation.pipeline import query_response_pipeline

def main():
    pdf_dir = Path(__file__).parent.parent / "data"
    print("Ingestion in process.....")

    sentences = init_pipeline(pdf_dir)
    print("Loaded PDF.....")
    chunked_documents = create_chunks(sentences)
    print("Chunked Sentences.....")
    client, embeddings = create_embeddings(chunked_documents)
    print("Retrieved Embeddings.....")

    should_update_pinecone = input("Do you want to write the embeddings to the vector db (Only do this if you have ingested new data): ")

    if(should_update_pinecone == "yes"):

        index = initialize_vector_store_pipeline(embeddings, True)
        print("Stored Embeddings.....")

    else:
        index = initialize_vector_store_pipeline(embeddings, False)
        print("Retrieved Embeddings.....")

    question = ""
    while(True):
        question = input("Ask your question or type 'end' to end the prompts: ")
        print()

        if(question == "end"):
            print("Bye Bye")
            break

        output = query_response_pipeline(client, index, question)

        print(output)
        print()


if __name__ == "__main__":
    main()