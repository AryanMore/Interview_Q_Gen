from resume_graph.build_resume_graph import build_graph
from neo4j import GraphDatabase
import os

def test_resume_graph_creation():
    build_graph("tests/sample_resume.pdf")

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    )

    with driver.session() as s:
        res = s.run("MATCH (c:Candidate) RETURN count(c) AS cnt")
        count = res.single()["cnt"]

    assert count >= 1
