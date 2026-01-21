from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from qdrant_client.http.models import PointStruct
from rag.qdrant_conn import client, COLLECTION
import os
from dotenv import load_dotenv

load_dotenv()


driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD")
    )
)

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def generate_probe(a, rel, b):
    """
    Convert domain relationship into interviewer knowledge
    """
    if rel == "HAS_CONCEPT":
        return f"Ask the candidate to explain the concept of {b} in the context of {a}."
    if rel == "CAUSES":
        return f"Probe the candidate about how {a} can lead to {b}."
    if rel == "MITIGATED_BY":
        return f"Ask how {b} helps mitigate issues related to {a}."
    return None


def insert_domain_knowledge():
    points = []
    idx = 0

    with driver.session() as s:
        result = s.run("""
        MATCH (a:Concept)-[r:HAS_CONCEPT|CAUSES|MITIGATED_BY]->(b:Concept)
        RETURN a.name AS source, type(r) AS rel, b.name AS target
        """)

        for row in result:
            text = generate_probe(row["source"], row["rel"], row["target"])
            if not text:
                continue

            vector = embedder.encode(text).tolist()

            points.append(
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload={
                        "text": text,
                        "source": row["source"],
                        "relation": row["rel"],
                        "target": row["target"]
                    }
                )
            )
            idx += 1

    if points:
        client.upsert(
            collection_name=COLLECTION,
            points=points
        )

    print(f"Inserted {len(points)} knowledge probes into Qdrant")


if __name__ == "__main__":
    insert_domain_knowledge()
