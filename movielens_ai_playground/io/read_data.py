import pandas as pd

def read_movies_data(path:str, sep="|"):
    data = pd.read_csv(path,
                       sep=sep,
                       encoding='latin-1',
                       header=None,
                       )
    data = data.iloc[:,[0,1]]
    data.columns = ["movieId", "title"]
    return data

if __name__ == "__main__":
    path = "/Users/tiago.cabo/Documents/github-repos/moviellens-ai-playground/data/movielens-100k/u.item"
    pd.read_csv(path, sep="|", encoding='latin-1', header=None).iloc[:, [0, 1]]

    read_movies_data(path)