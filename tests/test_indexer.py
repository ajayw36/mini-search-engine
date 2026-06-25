import unittest
from search_engine.indexer import build_index


class TestBuildIndex(unittest.TestCase):
    def test_single_document(self):
        documents = {"doc1.txt": "hello world"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(doc_lengths["doc1.txt"], 2)
        self.assertIn("hello", index)
        self.assertEqual(index["hello"]["doc1.txt"], 1)

    def test_multiple_documents(self):
        documents = {
            "doc1.txt": "hello world",
            "doc2.txt": "hello python"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(doc_lengths), 2)
        self.assertEqual(index["hello"]["doc1.txt"], 1)
        self.assertEqual(index["hello"]["doc2.txt"], 1)

    def test_term_frequency(self):
        documents = {"doc1.txt": "hello hello world"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(index["hello"]["doc1.txt"], 2)
        self.assertEqual(index["world"]["doc1.txt"], 1)

    def test_stop_words_excluded(self):
        documents = {"doc1.txt": "the quick brown fox"}
        index, doc_lengths = build_index(documents)

        self.assertNotIn("the", index)
        self.assertIn("quick", index)
        self.assertIn("brown", index)

    def test_document_length_count(self):
        documents = {"doc1.txt": "one two three four"}
        index, doc_lengths = build_index(documents)

        self.assertEqual(doc_lengths["doc1.txt"], 4)

    def test_empty_document(self):
        documents = {"doc1.txt": ""}
        index, doc_lengths = build_index(documents)

        self.assertNotIn("doc1.txt", doc_lengths)

    def test_document_with_only_stop_words(self):
        documents = {"doc1.txt": "the and is"}
        index, doc_lengths = build_index(documents)

        self.assertNotIn("doc1.txt", doc_lengths)
        self.assertEqual(len(index), 0)

    def test_case_insensitive_indexing(self):
        documents = {
            "doc1.txt": "Hello",
            "doc2.txt": "hello"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(index["hello"]), 2)

    def test_multiple_terms_across_documents(self):
        documents = {
            "doc1.txt": "python programming",
            "doc2.txt": "java programming",
            "doc3.txt": "python java"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(len(index["python"]), 2)
        self.assertEqual(len(index["programming"]), 2)
        self.assertEqual(len(index["java"]), 2)

    def test_term_appears_once_per_document(self):
        documents = {
            "doc1.txt": "search engine",
            "doc2.txt": "search algorithm"
        }
        index, doc_lengths = build_index(documents)

        self.assertEqual(index["search"]["doc1.txt"], 1)
        self.assertEqual(index["search"]["doc2.txt"], 1)


if __name__ == "__main__":
    unittest.main()
