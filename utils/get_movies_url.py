import csv
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

row_names = ['movie_id', 'movie_title']

df = pd.read_csv("data/movielens-100k-links/movie_poster.csv")

for idx, row in df.iterrows():
    movie_id = row['movieId']
    movie_title = row['title']
    domain = 'http://www.imdb.com'
    search_url = domain + '/find?q=' + urllib.parse.quote_plus(movie_title)
    with urllib.request.urlopen(search_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        # Get url of 1st search result
        try:
            title = soup.find('table', class_='findList').tr.a['href']
            movie_url = domain + title
            with open('movie_url.csv', 'a', newline='') as out_csv:
                writer = csv.writer(out_csv, delimiter=',')
                writer.writerow([movie_id, movie_url])
        # Ignore cases where search returns no results
        except AttributeError:
            pass