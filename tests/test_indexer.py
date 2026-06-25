import unittest
from search_engine.indexer import build_index


class TestBuildIndex(unittest.TestCase):
    def test_single_document(self):
        documents = {0: "hello world"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(doc_lengths[0], 2)
        self.assertIn("hello", index)
        self.assertEqual(index["hello"][0], 1)

    def test_multiple_documents(self):
        documents = {
            0: "hello world",
            1: "hello python"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(doc_lengths), 2)
        self.assertEqual(index["hello"][0], 1)
        self.assertEqual(index["hello"][1], 1)

    def test_term_frequency(self):
        documents = {0: "hello hello world"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(index["hello"][0], 2)
        self.assertEqual(index["world"][0], 1)

    def test_stop_words_excluded(self):
        documents = {0: "the quick brown fox"}
        index, doc_lengths = build_index(documents)

        self.assertNotIn("the", index)
        self.assertIn("quick", index)
        self.assertIn("brown", index)

    def test_document_length_count(self):
        documents = {0: "one two three four"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(doc_lengths[0], 4)

    def test_empty_document(self):
        documents = {0: ""}
        index, doc_lengths = build_index(documents)

        self.assertNotIn(0, doc_lengths)

    def test_document_with_only_stop_words(self):
        documents = {0: "the and is"}
        index, doc_lengths = build_index(documents)

        self.assertNotIn(0, doc_lengths)
        self.assertEqual(len(index), 0)

    def test_case_insensitive_indexing(self):
        documents = {
            0: "Hello",
            1: "hello"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(index["hello"]), 2)

    def test_multiple_terms_across_documents(self):
        documents = {
            0: "python programming",
            1: "java programming",
            2: "python java"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(index["python"]), 2)
        self.assertEqual(len(index["programming"]), 2)
        self.assertEqual(len(index["java"]), 2)

    def test_term_appears_once_per_document(self):
        documents = {
            0: "search engine",
            1: "search algorithm"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(index["search"][0], 1)
        self.assertEqual(index["search"][1], 1)


if __name__ == "__main__":
    unittest.main()
