from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from movielens_ai_playground.io.read_data import read_movies_data


class Qdrant:
    def __init__(self, host:str, port:int):
        self.client = QdrantClient(host=host,
                                    port=port)
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    def query_encode(self, query:str):
        return self.model.encode(query).tolist()

    def qdrant_feed(self):
        MOVIES_PATH = "data/movielens-100k/u.item"
        movies_df = read_movies_data(path=MOVIES_PATH)
        print(len(movies_df))
        self.client.recreate_collection(
            collection_name="movies_100k",
            vectors_config=models.VectorParams(
                size=self.model.get_sentence_embedding_dimension(),
                # Vector size is defined by used model
                distance=models.Distance.COSINE,
            ),
        )

        self.client.upload_records(
            collection_name="movies_100k",
            records=[
                models.Record(
                    id=idx, vector=self.model.encode(doc["title"],
                                                  normalize_embeddings=True).tolist(),
                    payload=doc.to_dict()
                )
                for idx, doc in movies_df.iterrows()
            ],
        )
    def qdrant_search(self, query:str, hits:int):
        results = self.client.search(
            collection_name="movies_100k",
            query_vector=self.query_encode(query=query),
            limit=hits,
        )
        return [id.id for id in results]