import os
from pathlib import Path

import numpy as np
import pandas as pd
import re

## bm25
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from movielens_ai_playground.semantic_search.bm25_preprocessing import nltk_process

# "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def encode_query_text(text):
    return model.encode(text, normalize_embeddings=True)


if __name__ == "__main__":
    path = "/Users/tiago.cabo/Documents/olx-projects/vespa-poc/ads/variant=base/run_id=2023-06-19T07"
    df = pd.DataFrame()
    for file in tqdm(os.listdir(path)):
        print(file)
        for cat in os.listdir(Path(path) / file):
            fullpath = Path(path) / file / cat
            tmp_df = pd.read_parquet(fullpath)
            tmp_df = tmp_df[:5000]
            df = pd.concat([df, tmp_df])

    pattern = re.compile("<.*?>")
    df["text"] = df.title + " " + df.description

    df["text"] = df.text.apply(lambda x: re.sub(pattern, "", x))

    df["embeddings"] = model.encode(df.text, normalize_embeddings=True).tolist()

    query = "gatos para dar"
    emb = model.encode(query, normalize_embeddings=True)

    # Compute cosine similarity between the encoded sentences
    cosine_scores = cosine_similarity(
        np.array(df.embeddings.tolist()), emb.reshape(1, -1)
    )
    # dot_score = emb.dot(np.array(df.embeddings.tolist()).T)
    # df["dot_score"] = dot_score
    df["cosine_score"] = cosine_scores

    df = df.sort_values(by="cosine_score", ascending=False)
    df.item_id[:10].values
    df.title
    tqdm.pandas()

    # bm25
    df["processed"] = df.text.progress_apply(nltk_process)

    bm25 = BM25Okapi(df["processed"])

    tokenized_query = nltk_process(query)

    doc_scores = bm25.get_scores(tokenized_query)
    sorted_indices = np.argsort(doc_scores)[::-1]
    bm25_df = df.iloc[sorted_indices]
    bm25_top = bm25_df.item_id[:50].values
