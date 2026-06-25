"""Command-line entry point for the mini search engine."""

from search_engine.search import SearchEngine
from search_engine.snippets import make_snippet
from search_engine.snippets import get_title

def main():
    engine = SearchEngine()

    print(f"Loaded {len(engine.documents)} documents.")
    print("Type a search query, or type 'quit' to exit.")

    while True:
        query = input("\nSearch: ")

        if query.lower() == "quit":
            break

        results = engine.search(query)

        if not results:
            print("No results found.")
            continue

        for position, (doc_id, score) in enumerate(results, start=1):
            doc_metadata = engine.get_doc(doc_id)
            text = doc_metadata["text"]
            doc_path = doc_metadata["path"]
            snippet = make_snippet(text, query)
            title = get_title(doc_path, text)
            print(f"{position}. {title} — score: {score:.4f}")
            print(f"   {snippet}")
            print()


if __name__ == "__main__":
    main()
