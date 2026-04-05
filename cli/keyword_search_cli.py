import argparse
from search_keyword import search_keyword_in_dataset
from load_data_set import load_data_set
from dotenv import load_dotenv
from pathlib import Path
import os

"""
This module's job is to parse arguments from the command line. For example, using the command:
--- uv run cli/keyword_search_cli.py search "${your search query}"--- 
will execute the "search" case and populate "your search query" into the args.query variable.
"""

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    args = parser.parse_args()

    base_file_path = Path(__file__).parent.parent
    data_set_filePath = os.getenv("DATA_SET_URL")
    if data_set_filePath == None:
        print(f"error fetching address to data set")
        return

    data_set = load_data_set(data_set_filePath, base_file_path)
    if data_set == None:
        return

    match args.command:
        case "search":
            search_keyword = args.query
            print(f"Searching for: {search_keyword}")
            search_keyword_in_dataset(search_keyword, data_set)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
