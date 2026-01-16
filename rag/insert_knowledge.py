from qdrant_client.http.models import PointStruct
from rag.qdrant_conn import client, COLLECTION, init_collection
from rag.embed import embed

init_collection()

data = [
 {"id":1,"text":"Vanishing gradients occur when gradients become very small during backpropagation.","skill":"CNN","difficulty":"medium"},
 {"id":2,"text":"Batch normalization normalizes activations to stabilize CNN training.","skill":"CNN","difficulty":"hard"},
 {"id":3,"text":"SQL indexing improves query performance.","skill":"SQL","difficulty":"easy"},
]

points=[]
for d in data:
    points.append(
        PointStruct(id=d["id"], vector=embed(d["text"]), payload=d)
    )

client.upsert(collection_name=COLLECTION, points=points)
print("Knowledge successfully inserted.")
