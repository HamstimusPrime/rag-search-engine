from filter_text import tokenize_text
from inverted_index import InvertedIndex


def search_keyword_in_dataset(query: str, inv_index: InvertedIndex):
    # iterate over each token in the query ☑️
    # use the index to get any documents mapped to the tokens
    # stop and return the do IDs when you have 5 matching documents
    # use the 5 IDs to fetch their documents and print the ID and Title fields of the docs
    inv_index.load()
    tokenized_query = tokenize_text(query)
    if not tokenized_query:
        return

    doc_id_list: list[str] = []

    for token in tokenized_query:
        doc_IDs = sorted(list(inv_index.index.get(token, [])))
        remaining = 5 - len(doc_id_list)
        print(f"")

        if remaining <= 0:
            break

        doc_id_list.extend(doc_IDs[:remaining])
    # use IDs to fetch docs from doc Maps
    for id in doc_id_list:
        mv_doc = inv_index.docmap[id]
        mv_ID = mv_doc["id"]
        mv_title = mv_doc["title"]
        print(f"movie ID: {mv_ID}. movie Title: {mv_title}")
