from neo4j import GraphDatabase

uri="bolt://localhost:7687"
auth=("neo4j","password")
driver=GraphDatabase.driver(uri,auth=auth)

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
