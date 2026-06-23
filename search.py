from pathlib import Path
import re
from collections import defaultdict

DOCS_DIR = Path("docs")

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
    return tokens

# Indexer - returns token --> set of docs
def build_index(documents):
    index = defaultdict(set)
    for doc_path, text in documents.items():
        for token in tokenize(text):
            index[token].add(doc_path)
    return index

# Match Count Ranking --> returns a list of documents ranked by score
def search(query, index):
    query_tokens = tokenize(query)
    ranker = defaultdict(int)
    for token in query_tokens:
        for doc in index[token]:
            ranker[doc] += 1

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

        for rank, (doc_path, score) in enumerate(results, start=1):
            print(f"{rank}. {doc_path} — score: {score}")