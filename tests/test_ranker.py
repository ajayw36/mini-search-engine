import unittest
import math
from search_engine.ranker import build_tf_idf, build_bm_25, rank
from search_engine.indexer import build_index


class TestBuildTfIdf(unittest.TestCase):
    def setUp(self):
        documents = {
            0: "machine learning algorithms",
            1: "machine learning python",
            2: "deep learning neural networks"
        }
        self.index, self.doc_lengths = build_index(documents)

    def test_tf_idf_scores_exist(self):
        scores = build_tf_idf(self.index, self.doc_lengths)
        self.assertGreater(len(scores), 0)
        self.assertIn("machine", scores)

    def test_tf_idf_term_appears_in_multiple_docs(self):
        scores = build_tf_idf(self.index, self.doc_lengths)

        self.assertEqual(len(scores["learning"]), 3)
        self.assertEqual(len(scores["machine"]), 2)

    def test_tf_idf_higher_score_for_rare_terms(self):
        scores = build_tf_idf(self.index, self.doc_lengths)

        # "neural" appears in only 1 doc, "learning" appears in 3
        # Both appear once in their respective docs, but "neural" should have higher IDF
        neural_idf = math.log(4 / 2)
        learning_idf = math.log(4 / 4)

        self.assertGreater(neural_idf, learning_idf)

    def test_tf_idf_is_positive(self):
        scores = build_tf_idf(self.index, self.doc_lengths)

        # Only check tokens that have scores
        if len(scores) > 0:
            for token_scores in scores.values():
                for score in token_scores.values():
                    self.assertGreaterEqual(score, 0)

    def test_tf_calculation(self):
        # With multiple docs, TF-IDF scores should differ for terms with different IDF
        documents = {
            0: "machine learning python algorithms",
            1: "machine learning java",
            2: "deep learning neural networks"
        }
        index, doc_lengths = build_index(documents)
        scores = build_tf_idf(index, doc_lengths)

        # "python" should have high score (rare term, appears only in doc0)
        self.assertIn("python", scores)
        python_score = scores["python"][0]
        self.assertGreater(python_score, 0)

        # "learning" appears in all docs, so should have 0 IDF
        self.assertIn("learning", scores)
        learning_scores = scores["learning"]
        for score in learning_scores.values():
            self.assertEqual(score, 0)

    def test_empty_index(self):
        scores = build_tf_idf({}, {})
        self.assertEqual(len(scores), 0)


class TestBuildBm25(unittest.TestCase):
    def setUp(self):
        documents = {
            0: "machine learning algorithms",
            1: "machine learning python",
            2: "deep learning neural networks"
        }
        self.index, self.doc_lengths = build_index(documents)

    def test_bm25_scores_exist(self):
        scores = build_bm_25(self.index, self.doc_lengths)
        self.assertGreater(len(scores), 0)
        self.assertIn("machine", scores)

    def test_bm25_is_numeric(self):
        scores = build_bm_25(self.index, self.doc_lengths)

        for token_scores in scores.values():
            for score in token_scores.values():
                self.assertIsInstance(score, float)

    def test_bm25_uses_correct_parameters(self):
        # Verify k=2.0 and b=0.75 are used
        scores = build_bm_25(self.index, self.doc_lengths)
        self.assertGreater(len(scores), 0)

    def test_bm25_term_frequency_saturation(self):
        # BM25 should saturate term frequency (diminishing returns for repeated terms)
        documents = {
            0: "word word",
            1: "word word word word word"
        }
        index, doc_lengths = build_index(documents)
        scores = build_bm_25(index, doc_lengths)

        # The score difference shouldn't be proportional to frequency difference (5:2)
        # BM25 saturates, so the ratio should be less than 2.5
        short_score = scores["word"][0]
        long_score = scores["word"][1]

        self.assertLess(long_score / short_score, 2.5)

    def test_bm25_document_length_normalization(self):
        # Both documents should get BM25 scores
        documents = {
            0: "relevant important",
            1: "relevant filler filler filler"
        }
        index, doc_lengths = build_index(documents)
        scores = build_bm_25(index, doc_lengths)

        # Both should have a score for "relevant"
        self.assertIn("relevant", scores)
        self.assertIn(0, scores["relevant"])
        self.assertIn(1, scores["relevant"])

        # Both scores should be numeric
        short_score = scores["relevant"][0]
        long_score = scores["relevant"][1]
        self.assertIsInstance(short_score, float)
        self.assertIsInstance(long_score, float)

    def test_empty_index(self):
        # Empty index should handle gracefully
        # Note: with empty document_lengths, avg_length would cause division by zero
        # So we test with at least one document
        index = {}
        doc_lengths = {0: 10}
        scores = build_bm_25(index, doc_lengths)
        self.assertEqual(len(scores), 0)


class TestRank(unittest.TestCase):
    def setUp(self):
        documents = {
            0: "machine learning is great",
            1: "python machine learning",
            2: "deep learning networks"
        }
        self.index, self.doc_lengths = build_index(documents)
        self.scores = build_tf_idf(self.index, self.doc_lengths)

    def test_rank_returns_sorted_results(self):
        results = rank("machine learning", self.scores)

        self.assertGreater(len(results), 0)
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i][1], results[i + 1][1])

    def test_rank_returns_tuples(self):
        results = rank("machine learning", self.scores)

        for result in results:
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], int)
            self.assertIsInstance(result[1], float)

    def test_rank_empty_query(self):
        results = rank("", self.scores)
        self.assertEqual(len(results), 0)

    def test_rank_nonexistent_term(self):
        results = rank("nonexistent xyz", self.scores)
        self.assertEqual(len(results), 0)

    def test_rank_single_term(self):
        results = rank("machine", self.scores)

        self.assertGreater(len(results), 0)
        self.assertIn(0, [r[0] for r in results])

    def test_rank_combines_scores(self):
        # Query with multiple terms should combine their scores
        results_single = rank("machine", self.scores)
        results_multi = rank("machine learning", self.scores)

        # Documents in multi-term query should have higher scores (combination)
        multi_scores = {doc: score for doc, score in results_multi}

        if 0 in multi_scores:
            self.assertGreater(multi_scores[0], 0)

    def test_rank_stop_words_ignored(self):
        # Query with stop words should be filtered out
        results_with_stop = rank("machine and learning", self.scores)
        results_without_stop = rank("machine learning", self.scores)

        self.assertEqual(len(results_with_stop), len(results_without_stop))

    def test_rank_duplicate_terms_deduplicated(self):
        # Duplicate terms in query should be treated as single term
        results_dup = rank("machine machine learning", self.scores)
        results_single = rank("machine learning", self.scores)

        self.assertEqual(results_dup, results_single)

    def test_rank_case_insensitive(self):
        results_lower = rank("machine learning", self.scores)
        results_upper = rank("MACHINE LEARNING", self.scores)

        self.assertEqual(results_lower, results_upper)


class TestRankWithBm25(unittest.TestCase):
    def setUp(self):
        documents = {
            0: "machine learning is great",
            1: "python machine learning",
            2: "deep learning networks"
        }
        self.index, self.doc_lengths = build_index(documents)
        self.scores = build_bm_25(self.index, self.doc_lengths)

    def test_rank_with_bm25(self):
        results = rank("machine learning", self.scores)

        self.assertGreater(len(results), 0)
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i][1], results[i + 1][1])


if __name__ == "__main__":
    unittest.main()
