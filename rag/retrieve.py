from rag.qdrant_conn import client, COLLECTION
from rag.embed import embed

def retrieve(concepts):
    vec = embed(" ".join(concepts))
    res = client.search(collection_name=COLLECTION, query_vector=vec, limit=5)
    return [r.payload["text"] for r in res]
