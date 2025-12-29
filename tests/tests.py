import unittest

from cli.keyword_search_cli import filter_text, tokenize_text


class Test_Filter_Text(unittest.TestCase):
    def test_filter_text(self):
        input_a = "It's Magic, Charlie Brown"
        expected_output_a = "its magic charlie brown"
        result = filter_text(input_a)
        self.assertEqual(expected_output_a, result)

    def test_tokenize_text(self):
        input_a = "The Matrix is a great movie!"
        expected_output_a = ["the", "matrix", "is", "a", "great", "movie"]
        result = tokenize_text(input_a)
        self.assertEqual(expected_output_a, result)


if __name__ == "__main__":
    unittest.main()
