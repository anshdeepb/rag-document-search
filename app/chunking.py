from langchain_text_splitters import NLTKTextSplitter
from langchain_core.documents import Document

def create_chunks(sentences):
    langchain_docs = [
    Document(
        page_content=sent["text"], 
        metadata={"source": sent["source"], "page": sent["page"]}
    ) 
    for sent in sentences
]

    text_splitter = NLTKTextSplitter( 
    chunk_size=800, 
    chunk_overlap=150,
)

    final_split_docs = text_splitter.split_documents(langchain_docs)

    chunked_documents = []

    for i, split_doc in enumerate(final_split_docs):
        if len(split_doc.page_content.strip()) < 40 and "Reading List" in split_doc.page_content:
            continue

        chunked_documents.append({
        "text": split_doc.page_content, 
        "source": split_doc.metadata["source"],
        "page": split_doc.metadata["page"],
        "chunk_id": f"{split_doc.metadata['source']}_{split_doc.metadata['page']}_{i}"
    })
    
    return chunked_documents

