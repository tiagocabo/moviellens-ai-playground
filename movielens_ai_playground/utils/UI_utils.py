import requests
import streamlit as st


def streamlit_image(image_path, title, description, no_description):
    st.markdown(f"#### {title}")
    try:
        st.image(image_path)
    except:
        pass

    if not no_description:
        st.markdown("## DESCRIÇÃO")
        with st.expander(description[:50]):
            st.write(description, unsafe_allow_html=True)


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


def plot_image(MAIN_IMAGE_ID, no_description=False):
    path, title, description = url_builder(MAIN_IMAGE_ID)
    streamlit_image(
        image_path=path,
        title=title,
        description=description,
        no_description=no_description,
    )

@st.cache_data
def plot_row_5(res, no_description=False):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        try:
            path, title, description = url_builder(int(res[0]))
            streamlit_image(
                image_path=path,
                title=title,
                description=description,
                no_description=no_description,
            )
            st.write(int(res[0]))
        except:
            pass
    with col2:
        try:
            path, title, description = url_builder(int(res[1]))
            streamlit_image(
                image_path=path,
                title=title,
                description=description,
                no_description=no_description,
            )
            st.write(int(res[1]))

        except:
            pass
    with col3:
        try:
            path, title, description = url_builder(int(res[2]))
            streamlit_image(
                image_path=path,
                title=title,
                description=description,
                no_description=no_description,
            )
            st.write(int(res[2]))

        except:
            pass

    with col4:
        try:
            path, title, description = url_builder(int(res[3]))
            streamlit_image(
                image_path=path,
                title=title,
                description=description,
                no_description=no_description,
            )
            st.write(int(res[3]))

        except:
            pass
    with col5:
        try:
            path, title, description = url_builder(int(res[4]))
            streamlit_image(
                image_path=path,
                title=title,
                description=description,
                no_description=no_description,
            )
            st.write(int(res[4]))

        except:
            pass
