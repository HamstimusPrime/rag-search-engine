#!/usr/bin/env python3
from pathlib import Path
import argparse, json, string, os
from dotenv import load_dotenv


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
        title_without_stopwords = remove_stopwords(movie_title)
        for movie in movie_list:
            # we check to see if at least one token from the tokenized user query matches at least one token from
            # the tokenized movie title
            if has_matching_tokens(
                tokenize_text(title_without_stopwords), tokenize_text(movie["title"])
            ):
                matching_movies.append(movie)

    if not matching_movies:
        print(f"no movies match the title: {movie_title}")
        return []

    matching_movies.sort(key=lambda x: int(x["id"]))
    return matching_movies


def remove_punctuation(text: str) -> str:
    text = text.lower()
    # get all punctuation strings and remove them from text
    translate_table = str.maketrans("", "", string.punctuation)
    filtered_text = text.translate(translate_table)
    return filtered_text


def tokenize_text(text: str) -> list[str]:
    filtered_text = remove_punctuation(text)
    return filtered_text.split(" ")


def has_matching_tokens(query_tokens: list[str], title_tokens: list[str]) -> bool:
    is_match = False
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False


def remove_stopwords(text: str) -> str:
    stopwords_url = os.getenv("STOP_WORD_PATH")
    if not stopwords_url:
        raise ValueError("STOP_WORD_PATH environment variable is not set")
    stopwords_list = load_stop_words(stopwords_url)

    text_without_punctuation = remove_punctuation(text)
    word_list = text_without_punctuation.split(" ")
    stopwords_set = {stopword.strip() for stopword in stopwords_list}
    filtered_text = [word for word in word_list if word not in stopwords_set]
    return " ".join(filtered_text)


def load_stop_words(file_address: str) -> list[str]:
    if not Path(file_address).exists():
        print(f"broken file path: {file_address}")
        return []
    with open(file_address, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    load_dotenv()
    main()
