from pathlib import Path

CORPUS_DIR = Path("corpus")


def load_documents(corpus_dir=CORPUS_DIR):
    """Load every Markdown file under `corpus_dir` keyed by its path."""
    documents = {}

    for file_path in Path(corpus_dir).rglob("*.md"):
        text = file_path.read_text("utf-8")
        documents[str(file_path)] = text

    return documents
