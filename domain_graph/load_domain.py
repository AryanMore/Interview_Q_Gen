from neo4j import GraphDatabase
import yaml
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


with open("seeds.yaml") as f:
    data = yaml.safe_load(f)

with driver.session() as s:

    for concept, details in data.items():

        # create main concept
        s.run("MERGE (c:Concept {name:$n})", n=concept)

        # sub concepts
        for sub in details.get("has_concept", []):
            s.run("""
            MERGE (a:Concept {name:$a})
            MERGE (b:Concept {name:$b})
            MERGE (a)-[:HAS_CONCEPT]->(b)
            """, a=concept, b=sub)

        # causes
        for c in details.get("causes", []):
            s.run("""
            MERGE (a:Concept {name:$a})
            MERGE (b:Concept {name:$b})
            MERGE (a)-[:CAUSES]->(b)
            """, a=concept, b=c)

print("Domain KG Loaded")
