from nltk.tokenize import sent_tokenize

def chunk_to_sentences(documents):
    sentences = []

    for doc in documents:
        for sent in sent_tokenize(doc["text"]):
            sentences.append({
                "text": sent,
                "source": doc["source"],
                "page": doc["page"]
            })

    return sentences