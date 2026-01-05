from text_utils import *
from text_utils import InvertedIndex
import argparse


def handler_search_comand(args: argparse.Namespace):
    print(f"Searching for: {args.query}")

    inverted_index = InvertedIndex()
    inverted_index.load()
    matching_movies = query_matches_index(args.query, inverted_index)
    for i in range(0, len(matching_movies)):
        print(
            f"{i+1}. {matching_movies[i]["title"]}:{matching_movies[i]["id"]}"
        )  # 1. Movie Title: $Movie ID


def handler_build_command():
    idx = InvertedIndex()
    idx.build()
    idx.save()


def handler_term_frequency(args: argparse.Namespace):
    (
        doc_id,
        term,
    ) = (
        args.id,
        args.term,
    )
    idx = InvertedIndex()
    idx.load()
    term_frequency = idx.get_tf(doc_id, term)
    print(f"the term ({term}) appears {term_frequency} times")
