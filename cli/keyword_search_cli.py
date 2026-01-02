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
    build_parser = subparsers.add_parser(
        "build", help="Build and save inverted index to disc"
    )

    search_parser.add_argument("query", type=str, help="Search query")
    # build_parser.add_argument("query", type=str, help="")

    args = parser.parse_args()

    match args.command:
        case "search":
            handler_search_comand(args)
        case "build":
            handler_build_command()
        case _:
            parser.print_help()


if __name__ == "__main__":
    load_dotenv()
    main()
