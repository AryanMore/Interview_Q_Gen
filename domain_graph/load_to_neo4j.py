from neo4j import GraphDatabase
import pandas as pd
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

df=pd.read_csv("domain_graph.csv")

def load():
    with driver.session() as s:
        for _,row in df.iterrows():
            rel = row.relation.upper()
            query = f"""
            MERGE (a:Concept {{name:$src}})
            MERGE (b:Concept {{name:$tgt}})
            MERGE (a)-[:{rel}]->(b)
            """
            s.run(query,src=row.source,tgt=row.target)

load()
print("Fixed Domain Graph Loaded.")
