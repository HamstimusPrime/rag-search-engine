import json
from pathlib import Path


def load_data_set(data_set_filePath: str, base_dir: Path) -> dict | None:
    if data_set_filePath == None:
        print(f"could not load data set. check address of data set")
        return
    abs_path = f"{base_dir}/{data_set_filePath}"
    with open(abs_path, "r") as f:
        data_set = json.load(f)

    return data_set
