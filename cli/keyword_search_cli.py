#!/usr/bin/env python3
from pathlib import Path
import argparse, json, string, os
from dotenv import load_dotenv
from text_utils import match_movies
from inverted_index import InvertedIndex


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
            movie_dataset_address = "data/movies.json"
            print(f"Searching for: {args.query}")
            matching_movies = match_movies(movie_dataset_address, args)
            if not matching_movies:
                return
            max_iterations = 5
            if len(matching_movies) < 5:
                max_iterations = len(matching_movies)
            for i in range(0, max_iterations):
                print(f"{i+1}. {matching_movies[i]["title"]} {i+1}")  # 1. Movie Title 1

        case "build":
            inverted_index = InvertedIndex()
            inverted_index.build()
            inverted_index.save()
            docs = inverted_index.get_documents("merida")
            # print a message containing the first ID of the document for the token
            print(f"First document for token 'merida' = {docs[0]}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    load_dotenv()
    main()
