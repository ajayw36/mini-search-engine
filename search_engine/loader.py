from pathlib import Path

CORPUS_DIR = Path("corpus")


def load_documents(corpus_dir=CORPUS_DIR):
    """Load every Markdown file under `corpus_dir` and assign stable doc IDs.

    Returns (documents, metadata) where:
    - documents: {doc_id: text}
    - metadata: {doc_id: {path: file_path, text: text}}
    """
    documents = {}
    metadata = {}
    doc_id = 0

    for file_path in sorted(Path(corpus_dir).rglob("*.md")):
        text = file_path.read_text("utf-8")
        documents[doc_id] = text
        metadata[doc_id] = {
            "path": str(file_path),
            "text": text,
        }
        doc_id += 1

    return documents, metadata
