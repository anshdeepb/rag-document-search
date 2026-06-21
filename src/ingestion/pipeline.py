from ingestion.pdf_loader import load_pdfs
from ingestion.chunker import chunk_to_sentences


def init_pipeline(path):

    documents = load_pdfs(path)
    sentences = chunk_to_sentences(documents)

    return(sentences)

