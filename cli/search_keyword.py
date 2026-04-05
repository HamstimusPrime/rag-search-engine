from filter_text import is_keyword_in_text


def search_keyword_in_dataset(keyword: str, data_set: dict) -> list[str] | None:
    if not data_set:
        return

    movie_titles_list = []
    for movie_obj in data_set["movies"]:
        if len(movie_titles_list) == 5:
            break

        movie_title = movie_obj["title"]
        if is_keyword_in_text(keyword, movie_title):
            movie_titles_list.append(movie_obj["title"])

    # print out movie title list
    for count, movie_title in enumerate(movie_titles_list, start=1):
        print(f"{count}. {movie_title} {count}")
