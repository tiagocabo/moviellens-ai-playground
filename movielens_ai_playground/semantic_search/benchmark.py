import pandas as pd
from sklearn.metrics import ndcg_score
from tqdm import tqdm

from movielens_ai_playground.semantic_search.bm25_retrieval import bm25_retrieve

path = "/Users/tiago.cabo/Documents/olx-projects/vespa-poc/ranking_benchmark_pt_day19.parquet"
df = pd.read_parquet(path)

# remove searches with filters
df = df[df.params_category_id.isna()]


def benchmark(bm25_k, total_products):
    k = 10
    res = []
    for query in tqdm(list(set(df.submitted_request))[:total_products]):
        # bm25 with title
        bm25_res_title = bm25_retrieve(query, hits=bm25_k, bm25_type="bm25_title")

        # bm25 with description
        bm25_res_title_desc = bm25_retrieve(
            query, hits=bm25_k, bm25_type="bm25_title_desc"
        )

        by_query_session_groups = (
            df.loc[
                df.submitted_request == query, ["meta_session_long", "ad_id", "rank"]
            ]
            .sort_values(by="rank")
            .groupby("meta_session_long")
        )

        for meta_session_long, group in by_query_session_groups:
            top_k_olx_results = group.head(k).ad_id.values

            cnt_title = 0
            for id in bm25_res_title:
                if id in top_k_olx_results:
                    cnt_title += 1

            cnt_title_desc = 0
            for id in bm25_res_title_desc:
                if id in top_k_olx_results:
                    cnt_title_desc += 1

            try:
                ndcg_val = ndcg_score(top_k_olx_results, bm25_res_title)
            except:
                ndcg_val = None
            res.append(
                {
                    "meta_session_long": meta_session_long,
                    "query": query,
                    "precision_title": cnt_title / k,
                    "precision_title_desc": cnt_title_desc / k,
                    "ndcg": ndcg_val,
                }
            )
    final_res = pd.DataFrame(res)
    final_res = final_res.sort_values(by="precision_title", ascending=False)
    return final_res


a = benchmark(10, 100)
b = benchmark(30, 15)
c = benchmark(10, 200)
d = benchmark(30, 200)
