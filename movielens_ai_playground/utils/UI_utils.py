import pandas as pd
import requests
import streamlit as st


def streamlit_image( title, genre, image_path=None):
    st.markdown(f"#### {title}")
    try:
        st.image(image_path)
    except:
        pass
    st.write(genre, unsafe_allow_html=True)


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
    MOVIES_PATH = "/Users/tiago.cabo/Documents/github-repos/moviellens-ai-playground/data/ml-25m/movies.csv"
    movies_df = pd.read_csv(MOVIES_PATH)
    title = movies_df.loc[movies_df.movieId == id, "title"]
    genre = movies_df.loc[movies_df.movieId == id, "genres"]
    return title, genre

def plot_image(MAIN_IMAGE_ID):
    title, genre = info_fetcher(MAIN_IMAGE_ID)
    streamlit_image(
        title=title,
        genre=genre,
    )

@st.cache_data
def plot_row_5(res):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        try:
            title, genre = info_fetcher(int(res[0]))
            streamlit_image(
                title=title,
                genre=genre,
            )
        except Exception as e:
            print(e)
            pass
    with col2:
        try:
            title, genre = info_fetcher(int(res[1]))
            streamlit_image(
                title=title,
                genre=genre,
            )

        except:
            pass
    with col3:
        try:
            title, genre = info_fetcher(int(res[2]))
            streamlit_image(
                title=title,
                genre=genre,
            )

        except:
            pass

    with col4:
        try:
            title, genre = info_fetcher(int(res[3]))
            streamlit_image(
                title=title,
                genre=genre,
            )

        except:
            pass
    with col5:
        try:
            title, genre = info_fetcher(int(res[4]))
            streamlit_image(
                title=title,
                genre=genre,
            )

        except:
            pass
