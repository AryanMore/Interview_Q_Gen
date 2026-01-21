from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import pdfplumber, re, yaml, os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))


driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

with open("config/skills_catalog.yaml") as f:
    CATALOG = yaml.safe_load(f)

SKILLS = []
for domain in CATALOG.values():
    SKILLS.extend(domain)

SKILLS = [s.lower() for s in SKILLS]

def extract_text(pdf):
    with pdfplumber.open(pdf) as p:
        return "\n".join([pg.extract_text() or "" for pg in p.pages])

def extract_entities(text):
    skills, projects = [], []
    text_lower = text.lower()


    for s in SKILLS:
        if re.search(rf"\b{s}\b", text_lower):
            skills.append(s.capitalize())


    for line in text.split("\n"):
        line_clean = line.strip()
        if is_valid_project(line_clean):
            projects.append(line_clean)

    return list(set(skills)), list(set(projects))

def cosine(a, b):
    return (a @ b) / (((a @ a) ** 0.5) * ((b @ b) ** 0.5))

def is_valid_project(line):
    l = line.lower()

    ignore = [
        "education","cgpa","percentage","class","coursework",
        "libraries","technologies","languages","overview:",
        "ssc","hsc","b.tech","vit","university","college"
    ]

    verbs = [
        "developed","built","created","designed","implemented",
        "system","platform","pipeline","model","ai","robot",
        "application","dashboard","automation","detection",
        "rag","classification","prediction"
    ]

    if any(i in l for i in ignore):
        return False

    return any(v in l for v in verbs) and len(line.split()) > 6

def build_graph(resume_path, candidate_id="test_candidate"):
    with driver.session() as s:
        s.run("""
        MATCH (c:Candidate {id:$cid})
        OPTIONAL MATCH (c)-[*]->(n)
        DETACH DELETE c, n
        """, cid=candidate_id)

    text = extract_text(resume_path)
    skills, projects = extract_entities(text)

    print("Skills:", skills)
    print("Projects:", projects)

    skill_vecs = {s: model.encode(s) for s in skills}
    proj_vecs = {p: model.encode(p) for p in projects}

    with driver.session() as s:
        s.run("MERGE (c:Candidate {id:$cid})", cid=candidate_id)

        for sk in skills:
            s.run("MERGE (s:Skill {name:$n})", n=sk)
            s.run("""
            MATCH (c:Candidate {id:$cid}), (s:Skill {name:$n})
            MERGE (c)-[:HAS_SKILL]->(s)
            """, cid=candidate_id, n=sk)

        for pr in projects:
            s.run("MERGE (p:Project {name:$n})", n=pr)
            s.run("""
            MATCH (c:Candidate {id:$cid}), (p:Project {name:$n})
            MERGE (c)-[:WORKED_ON]->(p)
            """, cid=candidate_id, n=pr)

        for p, pv in proj_vecs.items():
            for sk, sv in skill_vecs.items():
                if cosine(pv, sv) > 0.15:
                    s.run("""
                    MATCH (p:Project {name:$p}), (s:Skill {name:$s})
                    MERGE (p)-[:USES]->(s)
                    """, p=p, s=sk)

        for pr in projects:
            for sk in skills:
                if sk.lower() in pr.lower():
                    s.run("""
                    MATCH (p:Project {name:$p}), (s:Skill {name:$s})
                    MERGE (p)-[:USES]->(s)
                    """, p=pr, s=sk)

    print("Resume Knowledge Graph created.")

# ---------- CLI ----------
if __name__ == "__main__":
    build_graph("resume.pdf", candidate_id="local_test_candidate")
