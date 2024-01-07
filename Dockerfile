FROM python:3.11-slim as build

WORKDIR /code

COPY pyproject.toml poetry.lock ./

COPY movielens_ai_playground movielens_ai_playground
COPY data/movielens-100k/u.item data/movielens-100k/
COPY data/movielens-100k-links/movie_poster.csv data/movielens-100k-links/
COPY main.py README.md ./
COPY pages pages

# Project initialization:
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

FROM build as streamlit_app
EXPOSE 9090
CMD [ "streamlit", "run", "main.py", "--server.port", "9090", "--server.address",
 "0.0.0.0", "--server.headless", "true", "--server.fileWatcherType",
  "none", "--browser.gatherUsageStats", "false"]

FROM build as qdrant_feed
CMD ["python", "./movielens_ai_playground/semantic_search/qdrant_feed.py"]