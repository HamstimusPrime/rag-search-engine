import unittest, os
from dotenv import load_dotenv
from cli.text_utils import (
    remove_punctuation,
    tokenize_text,
    remove_stopwords,
    load_stop_words,
)


class Test_Filter_Text(unittest.TestCase):
    def test_filter_text(self):
        input_a = "It's Magic, Charlie Brown"
        expected_output_a = "its magic charlie brown"
        result = remove_punctuation(input_a)
        self.assertEqual(expected_output_a, result)

    def test_tokenize_text(self):
        input_a = "The Matrix is a great movie!"
        expected_output_a = ["the", "matrix", "is", "a", "great", "movie"]
        result = tokenize_text(input_a)
        self.assertEqual(expected_output_a, result)

    def test_remove_stop_words(self):
        load_dotenv()
        stopwords_url = os.getenv("STOP_WORD_PATH")
        if not stopwords_url:
            self.fail("could not load filepath from environment")

        stopword_list = load_stop_words(stopwords_url)
        input_a = "The Matrix is a great movie!"
        expected_output_a = "matrix great movie"
        result = remove_stopwords(input_a, stopword_list)
        self.assertEqual(expected_output_a, result)


if __name__ == "__main__":
    unittest.main()
