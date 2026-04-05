import string


def remove_punctuation_from_text(text: str) -> str:
    table = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(table)
    return cleaned_text


def process_text(text: str) -> str:
    return ""


def is_keyword_in_text(keyword: str, text: str) -> bool:
    clean_keywords = remove_punctuation_from_text(keyword).lower()
    clean_texts = remove_punctuation_from_text(text).lower()
    if clean_keywords in clean_texts:
        return True
    return False
