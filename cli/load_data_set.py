import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

base_dir = Path(__file__).parent.parent
data_set_filePath = os.getenv("DATA_SET_URL")
stopwords_filePath = os.getenv("STOP_WORDS")


def load_data_set() -> dict | None:
    abs_path = f"{base_dir}/{data_set_filePath}"
    if data_set_filePath == None:
        print(
            f"could not load data dataset from path{abs_path} check address of data set"
        )
        return

    with open(abs_path, "r") as f:
        data_set = json.load(f)

    return data_set


def load_stopwords() -> list | None:
    abs_path = f"{base_dir}/{stopwords_filePath}"
    if stopwords_filePath == None:
        print(f"could not load stopwords from path: {abs_path} check if file exists.")
        return
    with open(abs_path, "r") as f:
        stopwords = f.read().split("\n")

    return stopwords
