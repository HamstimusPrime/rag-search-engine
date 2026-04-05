import pytest
from cli.filter_text import remove_punctuation_from_text, is_keyword_in_text


@pytest.mark.parametrize(
    "a,expected",
    [
        ("hello! my name is Mo!!", "hello my name is Mo"),
        ("he!!-llo! my name is Mo!!", "hello my name is Mo"),
        ("It's Magic, Charlie Brown", "Its Magic Charlie Brown"),
    ],
)
def test_remove_punctuation(a, expected):
    assert remove_punctuation_from_text(a) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("magic charlie", "It's Magic, Charlie Brown", True),
    ],
)
def test_is_keyword_in_text(a, b, expected):
    assert is_keyword_in_text(a, b) == expected
