import pandas as pd
import requests
import streamlit as st

from movielens_ai_playground.io.read_data import read_movies_data


def streamlit_image( title, url=None):
    st.markdown(f"#### {title}")
    try:
        st.image(url)
    except:
        pass


def url_builder(id):
    resp = requests.get(f"https://www.olx.pt/api/v1/offers/{id}")
    try:
        image = resp.json()["data"]["photos"][0]
        image = image["link"].format(width=1000, height=750)
        title = resp.json()["data"]["title"]
        description = resp.json()["data"]["description"]
    except:
        image = ""
        title = "no image"
        description = "description"
    return image, title, description

def info_fetcher(id):
    MOVIES_PATH = "/Users/tiago.cabo/Documents/github-repos/moviellens-ai-playground/data/movielens-100k/u.item"
    movies_df = read_movies_data(path=MOVIES_PATH)
    title = movies_df.loc[movies_df.movieId == id, "title"].values[0]
    return title

def url_fetcher(id:int):
    MOVIES_URL_PATH = "/Users/tiago.cabo/Documents/github-repos/moviellens-ai-playground/data/movielens-100k-links/movie_poster.csv"
    df = pd.read_csv(MOVIES_URL_PATH, names=["movieId","url"])
    return df.loc[df.movieId == id, "url"].values[0]
def plot_image(MAIN_IMAGE_ID):
    title = info_fetcher(MAIN_IMAGE_ID)
    url = url_fetcher(MAIN_IMAGE_ID)
    streamlit_image(
        title=title,
        url=url,
    )

@st.cache_data
def plot_row_5(res):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        try:
            title = info_fetcher(int(res[0]))
            url = url_fetcher(id=int(res[0]))
            streamlit_image(
                title=title,
                url=url,
            )
        except Exception as e:
            print(e)
            pass
    with col2:
        try:
            title = info_fetcher(int(res[1]))
            url = url_fetcher(id=int(res[1]))
            streamlit_image(
                title=title,
                url=url,
            )

        except:
            pass
    with col3:
        try:
            title = info_fetcher(int(res[2]))
            url = url_fetcher(id=int(res[2]))
            streamlit_image(
                title=title,
                url=url,
            )

        except:
            pass

    with col4:
        try:
            title = info_fetcher(int(res[3]))
            url = url_fetcher(id=int(res[3]))
            streamlit_image(
                title=title,
                url=url,
            )

        except:
            pass
    with col5:
        try:
            title = info_fetcher(int(res[4]))
            url = url_fetcher(id=int(res[4]))
            streamlit_image(
                title=title,
                url=url,
            )

        except:
            pass
