from text_utils import tokenize_text, load_movie_list, Movie, create_file
from dotenv import load_dotenv
import os, logging, pickle


logger = logging.getLogger(__name__)


class InvertedIndex:
    def __init__(self) -> None:
        load_dotenv()
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, Movie] = {}

    def __add_documents(self, doc_id: int, text: str) -> None:
        tokenized_text = tokenize_text(text)
        for token in tokenized_text:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list:
        # get set of document IDs for a given token from the index.
        if not self.index:
            raise ValueError("empty index")
        matching_documents = list(self.index[term.lower()])
        if matching_documents:
            matching_documents.sort()
            return matching_documents
        return []

    def build(self) -> None:
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
        index_path = os.getenv("INDEX_PATH")
        doc_map_path = os.getenv("DOC_MAP_PATH")

        if not index_path or not doc_map_path:
            logger.error("could not load file path(s)")
            return

        index_file_path = create_file(index_path)
        doc_map_file_path = create_file(doc_map_path)

        # save the values in self.index and self.docmap
        with open(index_file_path, "wb") as f:
            pickle.dump(self.index, f)

        with open(doc_map_file_path, "wb") as f:
            pickle.dump(self.docmap, f)
