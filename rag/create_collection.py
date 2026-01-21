from qdrant_client.http import models
from qdrant_conn import client, COLLECTION

client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=models.VectorParams(
        size=384,      
        distance=models.Distance.COSINE
    )
)

print("Qdrant collection created")
