from neo4j import GraphDatabase

uri="bolt://localhost:7687"
auth=("neo4j","password")
driver=GraphDatabase.driver(uri,auth=auth)

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
