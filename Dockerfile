FROM python:3.11-slim

RUN pip install poetry
COPY pyproject.toml poetry.lock ./

COPY movielens_ai_playground movielens_ai_playground
COPY data/movielens-100k/u.item data/
COPY data/movielens-100k-links/movie_poster.csv data/
COPY main.py ./
RUN poetry install

CMD [ "streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]

