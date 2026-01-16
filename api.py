from fastapi import FastAPI, UploadFile, Form
from resume_graph.build_resume_graph import build_graph, driver   # <-- import driver
from rag.concept_expansion import expand_concepts
from rag.retrieve import retrieve
from rag.prompt_builder import build_prompt
from llm.generate_questions import generate
from rag.project_questions import project_prompt

import shutil, os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload_resume/")
async def upload_resume(file: UploadFile, role: str = Form(...)):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    build_graph(path)

    project_qs = []

    with driver.session() as s:
        pr = s.run("""
        MATCH (p:Project)
        OPTIONAL MATCH (p)-[:USES]->(s:Skill)
        RETURN p.name as project, collect(s.name) as skills
        """)

        projects = list(pr)
        print("PROJECTS FROM NEO4J:", projects)


    for p in projects:
        project_qs.append({
            "project": p["project"],
            "skills": p["skills"],
            "questions": project_prompt(p["project"], p["skills"])
        })
    

    concepts = expand_concepts()
    knowledge = retrieve(concepts)
    prompt = build_prompt([role], concepts, knowledge)
    skill_questions = generate(prompt)

    return {
        "role": role,

        "expanded_concepts": concepts,

        "skill_questions": skill_questions,

        "project_questions": project_qs
    }


@app.get("/health")
def health():
    return {"status": "running"}
