from pathlib import Path
import re
from collections import defaultdict
import math

DOCS_DIR = Path("docs")
STOP_WORDS = {
    "the", "and", "is", "in", "of", "to", "a", "an", "for", "on",
    "with", "as", "by", "at", "from", "this", "that", "it", "be"
}

# Data Source
def load_documents():
    documents = {}

    for file_path in DOCS_DIR.glob("*.md"):
        text = file_path.read_text("utf-8")
        documents[str(file_path)] = text

    return documents

# Parser / Tokenizer
def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [token for token in tokens if token not in STOP_WORDS]

# TF - IDF Index
def build_index(documents):
    tf_idf_index = defaultdict(dict)
    num_documents = len(documents)
    tokenized_documents = {}

    frequency_counter = defaultdict(lambda : defaultdict(int))
    for doc_path, text in documents.items():
        tokenized_text = tokenize(text)
        
        if not tokenized_text:
            continue

        tokenized_documents[doc_path] = tokenized_text

        for token in tokenized_text:
            frequency_counter[token][doc_path] += 1
        
    
    for token, document_counter in frequency_counter.items():
        for doc_path, count in document_counter.items():
            document_length = len(tokenized_documents[doc_path])
            tf = count / document_length

            docs_containing_token = len(document_counter)

            # Smoothing to avoid scores of 0
            idf = math.log ((num_documents + 1) / (docs_containing_token + 1)) + 1
        
            tf_idf_index[token][doc_path] = tf * idf
    
    return tf_idf_index

#  Ranking 
def search(query, index):
    query_tokens = tokenize(query)
    ranker = defaultdict(float)
    for token in query_tokens:
        if token not in index:
            continue
        for doc, score in index[token].items():
            ranker[doc] += score

    ranked_results = sorted(
        ranker.items(), 
        key=lambda item : item[1], 
        reverse = True
        )

    return ranked_results

    

if __name__ == "__main__":
    documents = load_documents()
    index = build_index(documents)

    print(f"Loaded {len(documents)} documents.")
    print("Type a search query, or type 'quit' to exit.")


    while True:
        query = input("\nSearch: ")

        if query.lower() == "quit":
            break

        results = search(query, index)

        if not results:
            print("No results found.")
            continue

        # Print the top 10 results
        for rank, (doc_path, score) in enumerate(results[:10], start=1):
            print(f"{rank}. {doc_path} — score: {score}")