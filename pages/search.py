import streamlit as st

from movielens_ai_playground.semantic_search.bm25_retrieval import bm25_retrieve
#from movielens_ai_playground.semantic_search.vespa_similar import vespa_semantic_search
from movielens_ai_playground.utils.UI_utils import plot_row_5

st.set_page_config(layout="wide")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        retrieval_option = st.selectbox(
            "Retrieval",
            ("paraphrase-multilingual-MiniLM-L12-v2", "bm25_title", "bm25_title_desc"),
        )

    with col2:
        N_option = st.selectbox("N", ("5", "10", "11"))

    with col3:
        reranker_option = st.selectbox("Re_Ranker", ("None", "a", "b"))

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        query = st.text_input("Query", "")
    with c2:
        search = st.button(
            "Search",
        )
if search:
    if retrieval_option == "paraphrase-multilingual-MiniLM-L12-v2":
        #res = vespa_semantic_search(query_text=query, hits=N_option)
        #ids = list(res.keys())
        raise NotImplementedError

    elif retrieval_option == "bm25_title":
        res = bm25_retrieve(query=query, hits=N_option, bm25_type=retrieval_option)
        ids = list(res)
    elif retrieval_option == "bm25_title_desc":
        #res = bm25_retrieve(query=query, hits=N_option, bm25_type=retrieval_option)
        #ids = list(res)
        raise NotImplementedError
    else:
        raise NotImplementedError

    st.write(
        f"Query {query}, retrieval {retrieval_option},"
        f" N {N_option}, reranker {reranker_option} "
    )
    st.write(f"Results {res}")
    if N_option:
        if int(N_option) % 5 == 0:
            for i in range(int(N_option) // 5):
                plot_row_5(ids[i * 5 : i * 5 + 5])

        else:
            for i in range(1 + int(N_option) // 5):
                plot_row_5(ids[i * 5 : i * 5 + 5])
