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

def map_skills():
    with driver.session() as s:
        s.run("""
        MATCH (s:Skill),(c:Concept)
        WHERE toLower(s.name)=toLower(c.name)
        MERGE (s)-[:MAPS_TO]->(c)
        """)
    print("Skill → Concept mapping done.")

if __name__=="__main__":
    map_skills()
