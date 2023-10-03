import pickle

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi

from movielens_ai_playground.semantic_search.bm25_preprocessing import nltk_process

MOVIES_PATH = "/Users/tiago.cabo/Documents/github-repos/moviellens-ai-playground/data/ml-25m/movies.csv"
movies_df = pd.read_csv(MOVIES_PATH)

print("Start building bm25 with titles")
bm25_title = BM25Okapi(movies_df.title)

# open a file, where you ant to store the data
file = open('bm25_title', 'wb')
pickle.dump(bm25_title, file=file)

file = open("bm25_title", "rb")

bm25_title = pickle.load(file)
# print("done")

def bm25_retrieve(query, hits, bm25_type = "bm25_title"):
    # preprocess query
    tokenized_query = nltk_process(query)
    print(tokenized_query)
    # fetch bm25 score
    if bm25_type == "bm25_title_desc":
        #doc_scores = bm25_title_desc.get_scores(tokenized_query)
        raise NotImplementedError
    elif bm25_type == "bm25_title":
        doc_scores = bm25_title.get_scores(tokenized_query)
        print(max(doc_scores))
    else:
        raise NotImplementedError("Please check bm25 type")

    # order by max
    sorted_indices = np.argsort(doc_scores)[::-1]
    print(sorted_indices)

    bm25_df = movies_df.iloc[sorted_indices]

    # get results
    bm25_top = bm25_df.movieId[: int(hits)].values
    return bm25_top

if  __name__ == "__main__":
    bm25_retrieve(query="car", hits=5, bm25_type="bm25_title")