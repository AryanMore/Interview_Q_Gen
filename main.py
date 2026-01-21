from rag.concept_expansion import expand_concepts
from rag.retrieve import retrieve
from rag.prompt_builder import build_prompt
from llm.generate_questions import generate
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

with driver.session() as s:
    result = s.run("""
    MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)
    RETURN collect(s.name) AS skills
    """)
    skills = result.single()["skills"]
concepts=expand_concepts()
knowledge=retrieve(concepts)

prompt=build_prompt(skills,concepts,knowledge)
questions=generate(prompt)

print("\nINTERVIEW QUESTIONS:\n",questions)
