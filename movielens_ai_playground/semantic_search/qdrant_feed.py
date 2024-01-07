from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

from movielens_ai_playground.io.read_data import read_movies_data

encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

qdrant = QdrantClient("qdrant", port=6333)

MOVIES_PATH = "data/movielens-100k/u.item"
movies_df = read_movies_data(path=MOVIES_PATH)

qdrant.recreate_collection(
    collection_name="movies_100k",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)

qdrant.upload_records(
    collection_name="movies_100k",
    records=[
        models.Record(
            id=idx, vector=encoder.encode(doc["title"],
                                          normalize_embeddings=True).tolist(),
            payload=doc.to_dict()
        )
        for idx, doc in movies_df.iterrows()
    ],
)

if __name__ == "__main__":
    hits = qdrant.search(
        collection_name="movies_100k",
        query_vector=encoder.encode("alien invasion").tolist(),
        limit=3,
    )
    for hit in hits:
        print(hit.payload, "score:", hit.score)