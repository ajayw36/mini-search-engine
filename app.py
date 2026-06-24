"""Command-line entry point for the mini search engine."""

from search_engine.search import SearchEngine


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

        for position, (doc_path, score) in enumerate(results, start=1):
            print(f"{position}. {doc_path} — score: {score}")


if __name__ == "__main__":
    main()
