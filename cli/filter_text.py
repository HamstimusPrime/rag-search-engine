import string
from load_data_set import load_stopwords
from dotenv import load_dotenv
from nltk.stem import PorterStemmer

load_dotenv()
stemmer = PorterStemmer()


def preprocess_text(text: str) -> str:
    text = text.lower()
    return remove_punctuation_from_text(text)


def remove_punctuation_from_text(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))


def filter_stopwords(keywords: list) -> list | None:
    kw_lower = [k.lower() for k in keywords]
    stopwords = load_stopwords()
    if not stopwords:
        return
    stopwords_set = set(stopwords)
    return [k for k in kw_lower if k not in stopwords_set]


def is_keyword_in_text(keyword: str, text: str) -> bool | None:
    # remove punctuations from both keywords and text data
    kw_without_punct = remove_punctuation_from_text(keyword).lower().split(" ")
    txt_without_punct = remove_punctuation_from_text(text).lower().split(" ")

    # remove stopwords after removing punctuations
    kw_without_stopwords = filter_stopwords(kw_without_punct)
    txt_without_stopwords = filter_stopwords(txt_without_punct)
    if not (txt_without_stopwords) or not (kw_without_stopwords):
        return

    # removed stemmed words from both keywords and text that have stopwords removed
    stemmed_kw = convert_words_to_stem(kw_without_stopwords)
    stemmed_txt = convert_words_to_stem(txt_without_stopwords)

    # check if processed keywords exists within processed text
    for kw in stemmed_kw:
        for txt in stemmed_txt:
            if kw in txt:
                return True
    return False


def convert_words_to_stem(words: list[str]):
    return [stemmer.stem(w) for w in words]


def tokenize_text(text: str) -> list[str] | None:
    processed_txt = preprocess_text(text)
    processed_words = processed_txt.split()
    words_without_stopwords = filter_stopwords(processed_words)
    if not words_without_stopwords:
        return
    stemmed_words = convert_words_to_stem(words_without_stopwords)
    filtered = [s for s in stemmed_words if s.strip()]
    return filtered
