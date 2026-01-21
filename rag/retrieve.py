from sentence_transformers import SentenceTransformer
from rag.qdrant_conn import client, COLLECTION
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

def retrieve(concepts, top_k=3):
    query = " ".join(concepts)
    vec = model.encode(query).tolist()

    hits = client.search(
        collection_name=COLLECTION,
        query_vector=vec,
        limit=top_k
    )

    return [h.payload["text"] for h in hits]
