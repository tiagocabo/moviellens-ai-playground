import os
import pickle
import re
from pathlib import Path

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
        df = pd.concat([df, tmp_df])

pattern = re.compile("<.*?>")

df["title_description"] = df.title + " " + df.description

tqdm.pandas()

df["title_description_processed"] = df.title_description.apply(
    lambda x: re.sub(pattern, "", x)
)
df["title_description_processed"] = df.title_description_processed.progress_apply(
    nltk_process
)

# df["title_processed"] = df.title.apply(lambda x: re.sub(pattern, "", x))
# df["title_processed"] = df.title_processed.progress_apply(nltk_process)

print("Start building bm25 with description")
bm25_title_desc = BM25Okapi(df["title_description_processed"])

# print("Start building bm25 without description")
# bm25_title = BM25Okapi(df["title_processed"])

# open a file, where you ant to store the data
# file = open("bm25_title", "wb")
# pickle.dump(bm25_title, file=file)

# open a file, where you ant to store the data
file = open("bm25_title_desc", "wb")
pickle.dump(bm25_title_desc, file=file)
