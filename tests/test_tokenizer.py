import unittest
from search_engine.tokenizer import tokenize


class TestTokenize(unittest.TestCase):
    def test_basic_tokenization(self):
        result = tokenize("hello world")
        self.assertEqual(result, ["hello", "world"])

    def test_lowercase_conversion(self):
        result = tokenize("Hello WORLD")
        self.assertEqual(result, ["hello", "world"])

    def test_stop_words_removed(self):
        result = tokenize("the quick brown fox")
        self.assertEqual(result, ["quick", "brown", "fox"])

    def test_punctuation_removed(self):
        result = tokenize("hello, world!")
        self.assertEqual(result, ["hello", "world"])

    def test_numbers_retained(self):
        result = tokenize("python3 version 2024")
        self.assertEqual(result, ["python3", "version", "2024"])

    def test_only_stop_words(self):
        result = tokenize("the and is in")
        self.assertEqual(result, [])

    def test_empty_string(self):
        result = tokenize("")
        self.assertEqual(result, [])

    def test_special_characters(self):
        result = tokenize("hello@world#test")
        self.assertEqual(result, ["hello", "world", "test"])

    def test_multiple_spaces(self):
        result = tokenize("hello    world")
        self.assertEqual(result, ["hello", "world"])

    def test_mixed_stop_words_and_content(self):
        result = tokenize("machine learning for data science")
        self.assertEqual(result, ["machine", "learning", "data", "science"])


if __name__ == "__main__":
    unittest.main()
