import os
import pickle
import re
from pathlib import Path

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from tqdm import tqdm

from movielens_ai_playground.semantic_search.bm25_preprocessing import nltk_process

path = "/Users/tiago.cabo/Documents/olx-projects/vespa-poc/ads/variant=base/run_id=2023-06-19T07"
df = pd.DataFrame()
for file in tqdm(os.listdir(path)):
    print(file)
    for cat in os.listdir(Path(path) / file):
        fullpath = Path(path) / file / cat
        tmp_df = pd.read_parquet(fullpath)
        tmp_df = tmp_df[:5000]
        df = pd.concat([df, tmp_df])
#
# # df = df[:5000]
# pattern = re.compile("<.*?>")
#
# #df["title_description"] = df.title + " " + df.description
#
# tqdm.pandas()
#
# #df["title_description_processed"] = df.title_description.apply(lambda x: re.sub(pattern, "", x))
# #df["title_description_processed"] = df.title_description_processed.progress_apply(nltk_process)
#
# df["title_processed"] = df.title.apply(lambda x: re.sub(pattern, "", x))
# df["title_processed"] = df.title_processed.progress_apply(nltk_process)
#
# #print("Start building bm25 with description")
# #bm25_title_desc = BM25Okapi(df["title_description_processed"])
#
# print("Start building bm25 without description")
# bm25_title = BM25Okapi(df["title_processed"])

# open a file, where you ant to store the data
# file = open('bm25_title', 'wb')
# pickle.dump(bm25_title, file=file)
file = open("bm25_title", "rb")
bm25_title = pickle.load(file)
# print("done")

# bm25_desc
file2 = open(
    "/Users/tiago.cabo/Documents/olx-projects/vespa-poc/semantic_search/bm25_title_desc",
    "rb",
)
bm25_title_desc = pickle.load(file2)


def bm25_retrieve(query, hits, bm25_type):
    # preprocess query
    tokenized_query = nltk_process(query)

    # fetch bm25 score
    if bm25_type == "bm25_title_desc":
        doc_scores = bm25_title_desc.get_scores(tokenized_query)
    elif bm25_type == "bm25_title":
        doc_scores = bm25_title.get_scores(tokenized_query)
    else:
        raise NotImplementedError("Please check bm25 type")

    # order by max
    sorted_indices = np.argsort(doc_scores)[::-1]
    bm25_df = df.iloc[sorted_indices]

    # get results
    bm25_top = bm25_df.item_id[: int(hits)].values
    return bm25_top
