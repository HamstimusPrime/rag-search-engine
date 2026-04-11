from filter_text import tokenize_text
from inverted_index import InvertedIndex


def search_keyword_in_dataset(query: str, inv_index: InvertedIndex):

    # iterate over each token in the query ☑️
    # use the index to get any documents mapped to the tokens
    # stop and return the do IDs when you have 5 matching documents
    # use the 5 IDs to fetch their documents and print the ID and Title fields of the docs
    inv_index.load()
    # tokenized_query = tokenize_text(query)
    # if not tokenized_query:
    #     return

    # would need a switch case for choosing which set operation to pick
    # based off of query condition if any
    # the index returns an ID set. that
    query_data = parse_query(query)
    if not query_data:
        return

    tokenized_query: list[str] = []
    for q in query_data.get("queries") or []:
        tokens = tokenize_text(q)
        if tokens:
            tokenized_query.extend(tokens)
        if not tokenized_query:
            return

    user_query = query_data.get("queries")
    query_condition = query_data.get("query_condition")

    print(
        f"user query = {user_query}\n{f"query condition is: '{query_condition}'" if query_condition is not None else ''}"
    )

    doc_id_list: list[str] = []

    # we use the query to search the inverted index for document IDs that match the token
    for token in tokenized_query:
        doc_IDs = sorted(list(inv_index.index.get(token, [])))
        print(
            f"sets that match token: {token} of ID {doc_IDs}is: {inv_index.index.get(token)}"
        )
        remaining = 5 - len(doc_id_list)

        if remaining <= 0:
            break
        doc_id_list.extend(doc_IDs[:remaining])

    # use IDs to fetch docs from doc Maps
    for id in doc_id_list:
        mv_doc = inv_index.docmap[id]
        mv_ID = mv_doc["id"]
        mv_title = mv_doc["title"]
        print(f"movie ID: {mv_ID}. movie Title: {mv_title}")


def parse_query(query: str) -> dict | None:
    query_conditions = ["AND", "NOT", "OR"]
    query_words = query.split(" ")
    parsed_words = [w for w in query_words if w.strip()]

    query_obj = {}

    if (len(parsed_words) == 3) and (parsed_words[1] in query_conditions):
        query_obj["queries"] = [parsed_words[0], parsed_words[2]]
        query_obj["query_condition"] = parsed_words[1]
        return query_obj

    if len(parsed_words) == 1:
        query_obj["queries"] = [parsed_words[0]]
        query_obj["query_condition"] = None

        return query_obj

    print(f"!!!invalid query: '{query}'. Please ensure to input a valid query...")
    return
