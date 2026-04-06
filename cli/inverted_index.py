import pickle, os, sys
from pathlib import Path
from filter_text import preprocess_text, tokenize_text
from load_data_set import load_data_set
from dotenv import load_dotenv


load_dotenv()

base_dir = Path(__file__).parent.parent
serialized_index_path = os.getenv("SERIALIZED_INDEX_PATH")
serialized_docmap_path = os.getenv("SERIALIZED_DOCMAP_PATH")


class InvertedIndex:
    def __init__(self) -> None:
        self.index: dict[str, set] = {}
        self.docmap: dict[str, dict] = {}
        self.abs_index_path = f"{base_dir}/{serialized_index_path}"
        self.abs_docmap_path = f"{base_dir}/{serialized_docmap_path}"

    def __add_document(self, doc_id: str, text: str):
        # tokenize string
        txt_tokens = tokenize_text(text)
        if not txt_tokens:
            return
        for txt in txt_tokens:
            if txt not in self.index:
                self.index[txt] = set()
            self.index[txt].add(doc_id)

    def build(self):
        # load movie dataset
        data_set = load_data_set()
        if not data_set:
            return

        for mv in data_set["movies"]:
            # --- build index using _add_document method  ---
            text = f"{mv["title"]} {mv["description"]}"

            mv_ID = mv["id"]
            self.__add_document(mv_ID, text)

            # --- build docmap ---
            self.docmap[mv["id"]] = mv

    def get_documents(self, term: str) -> list | None:
        if not self.index:
            print("error fetching documents. index not initialized")
            return
        # query the index dictionary and return a sorted list
        # of the document IDs that the term string appears in
        return sorted(self.index[term])

    def save(self):
        # this method serializes and writes to disk
        # the data that might already exist in both the document map and
        # the index using the pickle package
        if (not self.index) or (not self.docmap):
            print(f"error saving files. uninitialized index or document map")
            return

        print(f"dumping index to path: {self.abs_index_path}...")
        with open(self.abs_index_path, "wb") as file:
            pickle.dump(self.index, file)

        print(f"dumping docmap to path: {self.abs_docmap_path}...")
        with open(self.abs_docmap_path, "wb") as file:
            pickle.dump(self.docmap, file)

    def load(self):
        try:
            # --- load docmap ---
            with open(self.abs_docmap_path, "rb") as file:
                self.docmap = pickle.load(file)

            # --- load index ---
            with open(self.abs_index_path, "rb") as file:
                self.index = pickle.load(file)

        except Exception as e:
            print(f"error loading index and docmap, error: {e}")
            sys.exit(1)
