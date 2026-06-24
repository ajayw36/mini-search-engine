"""High-level orchestration: load the corpus, build the index, run queries."""

from search_engine.indexer import build_index
from search_engine.loader import CORPUS_DIR, load_documents
from search_engine.ranker import build_tf_idf, rank


class SearchEngine:
    def __init__(self, corpus_dir=CORPUS_DIR):
        self.documents = load_documents(corpus_dir)
        self.index, self.document_lengths = build_index(self.documents)
        # Score the whole corpus once, up front. Swap build_tf_idf for
        # another scorer (e.g. build_bm25) to change ranking methods.
        self.scores = build_tf_idf(self.index, self.document_lengths)

    def search(self, query, top_k=10):
        """Return the top `top_k` (doc_path, score) results for `query`."""
        results = rank(query, self.scores)
        return results[:top_k]
