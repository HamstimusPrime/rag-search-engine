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

    # --- Command: term frequency ---
    tf_parser = subparsers.add_parser(
        "tf", help="Builds inverted index and saves to disk"
    )
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to search for")

    # --- Command: inverted document frequency ---
    idf_parser = subparsers.add_parser(
        "idf",
        help="Returns an inverted frequency of appearances of the term in the dataset",
    )
    idf_parser.add_argument("term", type=str, help="Term to get socore for")

    # --- Command: TF IDF ---
    tf_idf_parser = subparsers.add_parser(
        "tfidf",
        help="Returns the tf_idf score or a term ",
    )
    tf_idf_parser.add_argument("doc_id", type=int, help="Document ID to search in")
    tf_idf_parser.add_argument("term", type=str, help="Term to search for")

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
            print("Building inverted index...")
            inverted_index.build()
            inverted_index.save()
            print("Inverted index built successfully.")
        case "tf":
            doc_id = args.doc_id
            search_term = args.term
            tf = inverted_index.get_tf(doc_id, search_term)
            print(
                f"the term {search_term} has a frequency of {tf} in document with ID of {doc_id}"
            )
        case "idf":
            search_term = args.term
            idf = inverted_index.calculate_idf(search_term)
            print(f"Inverse document frequency of '{search_term}': {idf:.2f}")
        case "tfidf":
            tf_idf = inverted_index.calculate_tf_idf(args.doc_id, args.term)
            print(
                f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}"
            )
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
