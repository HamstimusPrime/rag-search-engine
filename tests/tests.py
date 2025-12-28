import unittest

from cli.keyword_search_cli import filter_text


class Test_Filter_Text(unittest.TestCase):
    def test_filter_punctuations(self):
        input_a = "It's Magic, Charlie Brown"
        expected_output_a = "its magic charlie brown"
        result = filter_text(input_a)
        self.assertEqual(expected_output_a, result)


if __name__ == "__main__":
    unittest.main()
