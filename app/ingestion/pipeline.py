from ingestion.pdf_loader import load_pdfs


def init_pipeline(path):
    return load_pdfs(path)