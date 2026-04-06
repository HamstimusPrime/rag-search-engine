import argparse
from search_keyword import search_keyword_in_dataset
from load_data_set import load_data_set, load_stopwords
from dotenv import load_dotenv
from inverted_index import InvertedIndex


"""
This module's job is to parse arguments from the command line. For example, using the command:
--- uv run cli/keyword_search_cli.py search "${your search query}"--- 
will execute the "search" case and populate "your search query" into the args.query variable.
"""

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Command: search ---
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    # --- Command: build ---
    build_parser = subparsers.add_parser(
        "build", help="builds inverted index and saves to disk"
    )

    args = parser.parse_args()
    data_set = load_data_set()

    if data_set == None:
        return

    inverted_index = InvertedIndex()
    match args.command:
        case "search":
            search_keyword = args.query
            print(f"Searching for: {search_keyword}")
            search_keyword_in_dataset(search_keyword, inverted_index)
        case "build":
            inverted_index.build()
            inverted_index.save()
            docs = inverted_index.get_documents("merida")
            if not docs:
                return

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
