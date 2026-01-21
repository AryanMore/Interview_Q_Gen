from neo4j import GraphDatabase

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

def expand_concepts():
    with driver.session() as s:
        result = s.run("""
        MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)-[:MAPS_TO]->(k:Concept)
        MATCH path=(k)-[:HAS_CONCEPT|CAUSES|MITIGATED_BY*1..3]->(x)
        RETURN DISTINCT x.name
        """)
        return [r["x.name"] for r in result]

if __name__=="__main__":
    concepts = expand_concepts()
    print("Expanded Concepts:", concepts)
