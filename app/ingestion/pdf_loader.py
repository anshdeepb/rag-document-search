from pypdf import PdfReader
from pathlib import Path
from ingestion.text_cleaner import clean_text

def load_pdfs(path):
    
    pdf_data = path

    documents = []

    for file in sorted(pdf_data.glob("*.pdf")):
        reader = PdfReader(file)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()

            if text:
                text = clean_text(text)

                documents.append({
                "text": text,
                "source": file.name,
                "page": i
            })
    return documents