"""High-level orchestration: load the corpus, build the index, run queries."""

from search_engine.indexer import build_index
from search_engine.loader import CORPUS_DIR, load_documents
from search_engine.ranker import build_tf_idf, build_bm_25, rank
from search_engine.tokenizer import tokenize
from search_engine.persistence import load_index, save_index


class SearchEngine:
    def __init__(self, corpus_dir=CORPUS_DIR):
        self.documents = load_documents(corpus_dir)

        # Try to load from cache first
        self.index, self.document_lengths, self.scores = load_index()

        if self.index is None:
            # Cache miss, rebuild and save
            self.index, self.document_lengths = build_index(self.documents)
            self.scores = build_bm_25(self.index, self.document_lengths)
            save_index(self.index, self.document_lengths, self.scores)

    def search(self, query, top_k=3):
        """Return the top `top_k` (doc_path, score) results for `query`."""
        results = rank(query, self.scores)
        return results[:top_k]
