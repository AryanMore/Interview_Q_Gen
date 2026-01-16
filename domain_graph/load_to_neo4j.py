from neo4j import GraphDatabase
import pandas as pd

uri="bolt://localhost:7687"
auth=("neo4j","password")
driver=GraphDatabase.driver(uri,auth=auth)

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
