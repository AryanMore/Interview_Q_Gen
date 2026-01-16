from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import pdfplumber, re, yaml

model = SentenceTransformer("all-MiniLM-L6-v2")

NEO4J_URI="bolt://localhost:7687"
NEO4J_AUTH=("neo4j","password")
driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

with open("config/skills_catalog.yaml") as f:
    CATALOG = yaml.safe_load(f)

SKILLS=[]
for domain in CATALOG.values():
    SKILLS.extend(domain)

SKILLS=[s.lower() for s in SKILLS]


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


def cosine(a,b):
    return (a@b)/(((a@a)**0.5)*((b@b)**0.5))

def is_valid_project(line):
    l = line.lower()

    ignore = [
        "education","cgpa","percentage","class","coursework",
        "libraries","technologies","languages","overview:",
        "ssc","hsc","b.tech","university","college"
    ]

    verbs = [
        "developed","built","created","designed","implemented",
        "system","platform","pipeline","model","ai","robot",
        "application","dashboard","automation","detection",
        "rag","classification","prediction"
    ]

    if any(i in l for i in ignore):
        return False

    if any(v in l for v in verbs) and len(line.split()) > 6:
        return True

    return False


def build_graph(resume_path):
    text = extract_text(resume_path)
    skills, projects = extract_entities(text)

    print("Skills:", skills)
    print("Projects:", projects)

    skill_vecs={s:model.encode(s) for s in skills}
    proj_vecs={p:model.encode(p) for p in projects}

    with driver.session() as s:
        s.run("MERGE (c:Candidate {name:'Candidate_1'})")

        for sk in skills:
            s.run("MERGE (s:Skill {name:$n})", n=sk)
            s.run("""
            MATCH (c:Candidate {name:'Candidate_1'}),(s:Skill {name:$n})
            MERGE (c)-[:HAS_SKILL]->(s)
            """, n=sk)

        for pr in projects:
            s.run("MERGE (p:Project {name:$n})", n=pr)
            s.run("""
            MATCH (c:Candidate {name:'Candidate_1'}),(p:Project {name:$n})
            MERGE (c)-[:WORKED_ON]->(p)
            """, n=pr)

        for p,pv in proj_vecs.items():
            for sk,sv in skill_vecs.items():
                if cosine(pv,sv) > 0.15:
                    s.run("""
                    MATCH (p:Project {name:$p}),(s:Skill {name:$s})
                    MERGE (p)-[:USES]->(s)
                    """, p=p, s=sk)

        # ---- Fallback rule ----
        for pr in projects:
            for sk in skills:
                if sk.lower() in pr.lower():
                    s.run("""
                    MATCH (p:Project {name:$p}),(s:Skill {name:$s})
                    MERGE (p)-[:USES]->(s)
                    """, p=pr, s=sk)


    print("Resume Knowledge Graph created.")

if __name__=="__main__":
    build_graph("resume.pdf")
