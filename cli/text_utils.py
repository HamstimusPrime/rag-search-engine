from nltk.stem import PorterStemmer
import argparse, json, string, os, logging, pickle
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)


class Movie(TypedDict):
    id: int
    title: str
    description: str


def match_movies(file_address: str, parsed_args: argparse.Namespace) -> list:
    stopwords_url = os.getenv("STOP_WORD_PATH")
    movie_list_url = os.getenv("MOVIE_LIST_PATH")

    if not movie_list_url:
        raise ValueError("MOVIE_LIST_PATH environment variable is not set")

    if not stopwords_url:
        raise ValueError("STOP_WORD_PATH environment variable is not set")

    # check if file exists
    if not Path(file_address).exists():
        print(f"broken file path: {file_address}")
        return []

    movie_title = parsed_args.query
    matching_movies = []

    stopwords_list = load_stop_words(stopwords_url)
    title_without_stopwords = remove_stopwords(movie_title, stopwords_list)
    stemmed_title = generate_stem_word(title_without_stopwords)

    movie_list = load_movie_list(movie_list_url)
    if not movie_list:
        raise ValueError("STOP_WORD_PATH environment variable is not set")

    for movie in movie_list:
        # we check to see if at least one token from the tokenized user query matches at least one token from
        # the tokenized movie title
        if has_matching_tokens(
            tokenize_text(stemmed_title), tokenize_text(movie["title"])
        ):
            matching_movies.append(movie)

    if not matching_movies:
        print(f"no movies match the title: {movie_title}")
        return []

    matching_movies.sort(key=lambda x: int(x["id"]))
    return matching_movies


def remove_punctuation(text: str) -> str:
    # get all punctuation strings and remove them from text
    text = text.lower()
    translate_table = str.maketrans("", "", string.punctuation)
    return text.translate(translate_table)


def tokenize_text(text: str) -> list[str]:
    filtered_text = remove_punctuation(text)
    return filtered_text.split(" ")


def has_matching_tokens(query_tokens: list[str], title_tokens: list[str]) -> bool:
    is_match = False
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False


def remove_stopwords(text: str, stopwords_list: list[str]) -> str:
    text_without_punctuation = remove_punctuation(text)
    word_list = text_without_punctuation.split(" ")
    stopwords_set = {stopword.strip() for stopword in stopwords_list}
    filtered_text = [word for word in word_list if word not in stopwords_set]
    return " ".join(filtered_text)


def load_stop_words(file_address: str) -> list[str]:
    if not Path(file_address).exists():
        print(f"broken file path: {file_address}")
        return []
    with open(file_address, "r") as f:
        return f.read().split("\n")


def generate_stem_word(word) -> str:
    stemmer = PorterStemmer()
    return stemmer.stem(word)


def load_movie_list(file_url: str) -> list[Movie]:
    with open(file_url, "r") as f:
        movie_list = json.load(f)["movies"]

    if movie_list:
        return movie_list

    return []


def create_file(file_path: str) -> str:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    return file_path


def query_matches_index(query: str, inverted_index: InvertedIndex) -> list:
    # should return a list of Movie Objects
    # return 5 items from the document
    matching_documents = []
    seen_ids = set()

    processed_token_list = process_token(query)

    for token in processed_token_list:
        if token in inverted_index.index:
            matching_documents_index_list = inverted_index.get_documents(token)
            for index in matching_documents_index_list:
                if index not in seen_ids:
                    matching_documents.append(inverted_index.docmap[index])
                    seen_ids.add(index)
                    if len(matching_documents) == 5:
                        return matching_documents
    print("no matches found")
    return matching_documents


def process_token(query: str) -> list[str]:
    stopwords_url = os.getenv("STOP_WORD_PATH")
    movie_list_url = os.getenv("MOVIE_LIST_PATH")
    if not movie_list_url:
        raise ValueError("MOVIE_LIST_PATH environment variable is not set")
    if not stopwords_url:
        raise ValueError("STOP_WORD_PATH environment variable is not set")

    processed_token = []
    tokenized_query = tokenize_text(query)

    for token in tokenized_query:
        stemmed_token = generate_stem_word(token)
        processed_token.append(stemmed_token)
    return processed_token


class InvertedIndex:
    def __init__(self) -> None:
        load_dotenv()
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, Movie] = {}
        self.term_frequencies: dict[int, Counter] = defaultdict(Counter)
        self.index_path: str | None = os.getenv("INDEX_PATH")
        self.docmap_path: str | None = os.getenv("DOC_MAP_PATH")
        self.term_frequency_path: str | None = os.getenv("TERM_FREQUENCY_PATH")

    def __add_documents(self, doc_id: int, text: str) -> None:
        processed_text = process_token(text)
        for token in set(processed_text):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)  # e.g -> {cat : set(3 ,8, 61)}
        # for each token, update its term frequency
        if doc_id not in self.term_frequencies:
            self.term_frequencies[doc_id] = Counter()
        for token in processed_text:
            self.term_frequencies[doc_id].update([token])

    def get_documents(self, term: str) -> list[int]:
        # get set of document IDs for a given token from the index.
        doc_ids = self.index.get(term, set())
        return sorted(list(doc_ids))

    def build(self) -> None:
        # build expects to work on a JSON
        movie_list_url = os.getenv("MOVIE_LIST_PATH")
        if not movie_list_url:
            logger.error("unable to fetch path to movie dataset")
            return
        movie_list = load_movie_list(movie_list_url)
        for movie in movie_list:
            # should iterate over all of the movies and add them to doc map and index
            # add movie object to docmap
            self.docmap[movie["id"]] = movie
            input = f"{movie['title']} {movie['description']}"
            self.__add_documents(int(movie["id"]), input)

    def save(self) -> None:
        # create file_directory to store
        if not self.index_path or not self.docmap_path or not self.term_frequency_path:
            logger.error("could not load file path(s) to documents")
            return

        index_file_path = create_file(self.index_path)
        doc_map_file_path = create_file(self.docmap_path)

        term_freq_file_path = create_file(self.term_frequency_path)

        # save the values in self.index and self.docmap
        with open(index_file_path, "wb") as f:
            pickle.dump(self.index, f)

        with open(doc_map_file_path, "wb") as f:
            pickle.dump(self.docmap, f)

        ##------ save the term frequency attribute to disk -----##
        if not self.term_frequencies:
            return
        with open(term_freq_file_path, "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def get_tf(self, doc_id: int, term: str) -> int:
        processed_term = process_token(term)
        if len(processed_term) > 1:
            raise Exception("term contains more than one token")
        token = processed_term[0]
        if doc_id not in self.term_frequencies:
            logger.error(f"no document with id:{doc_id} in dataset")
            return 0

        return self.term_frequencies[doc_id][token]

    def load(self) -> None:
        if not self.index_path or not self.docmap_path or not self.term_frequency_path:
            raise Exception("problem with document file path")

        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

        with open(self.term_frequency_path, "rb") as f:
            self.term_frequencies = pickle.load(f)
