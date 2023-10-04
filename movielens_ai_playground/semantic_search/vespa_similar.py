import urllib.parse

import requests

from semantic_search.generate_semantic_embeddings import encode_query_text
from similar_ads_search import parse_embedding


def query_semantic_embedding(ad_id):
    yql = 'select * from query where id contains "{}"'.format(ad_id)
    url = "http://localhost:8080/search/?yql={}&hits=1".format(
        urllib.parse.quote_plus(yql)
    )
    result = requests.get(url).json()
    result = parse_embedding(result["root"]["children"][0])
    return result


def query_semantic_similar(item_vector, hits):
    nn_annotations = ["targetHits:{}".format(hits)]
    nn_annotations = "{" + ",".join(nn_annotations) + "}"
    nn_search = "({}nearestNeighbor(embedding, item_embedding))".format(nn_annotations)

    data = {
        "hits": hits,
        "yql": "select id from query where {}".format(nn_search),
        "input.query(item_embedding)": item_vector,
        "ranking.profile": "semantic_similarity",
    }
    return requests.post("http://localhost:8080/search/", json=data).json()


def vespa_semantic_search(query_text, hits=10):
    user_vector = encode_query_text(query_text)
    user_vector = list(map(float, user_vector))
    result = query_semantic_similar(user_vector, int(hits) + 1)
    similar_products = {}
    for res in result["root"]["children"]:
        similar_products[res["fields"]["id"]] = res["relevance"]
    return similar_products
