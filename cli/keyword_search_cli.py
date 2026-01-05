#!/usr/bin/env python3
from pathlib import Path
import argparse, json, string, os
from dotenv import load_dotenv
from text_utils import match_movies
from handlers import *


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    term_frequency_parser = subparsers.add_parser(
        "tf", help="get frequency for term within the document of the ID provided"
    )
    build_parser = subparsers.add_parser(
        "build", help="Build and save inverted index to disc"
    )

    search_parser.add_argument("query", type=str, help="Search query")
    term_frequency_parser.add_argument("id", type=int, help="Document ID to query")
    term_frequency_parser.add_argument(
        "term", type=str, help="Word to find frequency for"
    )
    # build_parser.add_argument("query", type=str, help="")

    args = parser.parse_args()

    match args.command:
        case "search":
            handler_search_comand(args)
        case "build":
            handler_build_command()
        case "tf":
            handler_term_frequency(args)
        case _:
            parser.print_help()


if __name__ == "__main__":
    load_dotenv()
    main()
