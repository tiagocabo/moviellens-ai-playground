import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm
from vespa.deployment import VespaDocker
from generate_semantic_embeddings import encode_query_text

vespa_docker = VespaDocker()

app = vespa_docker.deploy_from_disk(
    "ads", "vespa-poc/vespa_config"
)

path = "ads/variant=base/run_id=2023-06-19T07"
for file in tqdm(os.listdir(path)):
    # if file == "category=10":
    for cat in os.listdir(Path(path) / file):
        fullpath = Path(path) / file / cat
        print(fullpath)
        df = pd.read_parquet(fullpath)
        print(f"Total df size is {len(df)}")

        df = df[:5000]
        df = df.rename(columns={"item_id": "id"})

        # split into 100 chunks to evaluate if encodes faster
        for k, chunk in tqdm(df.groupby(np.arange(len(df)) // 5000)):
            chunk = chunk.reset_index(drop=True)
            chunk["embedding"] = encode_query_text(
                chunk.title + " " + chunk.description
            ).tolist()
            res = app.feed_df(df=chunk[["id", "embedding"]], schema="query")
