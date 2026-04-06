import string
from load_data_set import load_stopwords
from dotenv import load_dotenv
from nltk.stem import PorterStemmer

load_dotenv()
stemmer = PorterStemmer()


def preprocess_text(text: str):
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
    stemmed_kw = [stemmer.stem(k) for k in kw_without_stopwords]
    stemmed_txt = [stemmer.stem(t) for t in txt_without_stopwords]

    # check if processed keywords exists within processed text
    for kw in stemmed_kw:
        for txt in stemmed_txt:
            if kw in txt:
                return True
    return False
