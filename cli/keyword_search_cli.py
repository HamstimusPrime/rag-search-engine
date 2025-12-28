#!/usr/bin/env python3
from pathlib import Path
import argparse, json, string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

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
        case _:
            parser.print_help()


def match_movies(file_address: str, parsed_args: argparse.Namespace) -> list:
    # check if file exists
    if not Path(file_address).exists():
        print(f"broken file path: {file_address}")
        return []

    movie_title = parsed_args.query
    matching_movies = []
    with open(file_address, "r") as f:
        movie_list = json.load(f)["movies"]
        for movie in movie_list:
            if filter_text(movie_title) in filter_text(movie["title"]):
                matching_movies.append(movie)

    if not matching_movies:
        print(f"no movies match the title: {movie_title}")
        return []

    matching_movies.sort(key=lambda x: x["id"])
    return matching_movies


def filter_text(text: str) -> str:
    text = text.lower()
    # get all punctuation strings and

    translate_table = str.maketrans("", "", string.punctuation)
    filtered_text = text.translate(translate_table)
    return filtered_text


if __name__ == "__main__":
    main()
