# Context-Aware Interview Question Generator

This project generates intelligent, personalized interview questions from a candidate resume using:

- Resume Knowledge Graph (Neo4j)  
- Domain Knowledge Graph  
- Local LLM (Ollama)  
- Streamlit Frontend + FastAPI Backend  

The system focuses on producing **project-aware and role-specific questions** instead of generic LLM outputs.

---

## Project Workflow

1. **Resume Upload**
   - Recruiter uploads a PDF resume and selects the target job role.

2. **Resume Parsing**
   - Text is extracted using pdfplumber.
   - Skills are detected using a curated skills catalog.
   - Project descriptions are identified from the resume.

3. **Resume Knowledge Graph Creation**
   - A graph is built in Neo4j containing:
     - Candidate node  
     - Skill nodes  
     - Project nodes  
   - Relationships created:
     - Candidate ──HAS_SKILL──▶ Skill  
     - Candidate ──WORKED_ON──▶ Project  
     - Project ──USES──▶ Skill  

4. **Concept Expansion**
   - Detected skills are mapped to the Domain Knowledge Graph.
   - Related technical concepts are expanded to ensure depth and progression in questioning.

5. **LLM Question Generation**
   - Two categories of questions are produced:
     - Skill / theory questions  
     - Project-specific questions grounded in the candidate’s experience  

6. **Frontend Display**
   - Streamlit interface displays:
     - Expanded concepts  
     - Skill questions  
     - Project questions

---

## Two Knowledge Graphs – Purpose

### 1) Resume Knowledge Graph (Dynamic)

**File:** `resume_graph/build_resume_graph.py`

**Represents:**
- Facts extracted from the candidate resume.

**Nodes**
- Candidate  
- Skills  
- Projects  

**Relations**
- HAS_SKILL  
- WORKED_ON  
- USES  

**Role**
- Grounds the system to the candidate’s real experience  
- Enables project-focused questioning  
- Prevents hallucinated skills

---

### 2) Domain Knowledge Graph (Static)

**File:** `domain_graph/seeds.yaml` (or loader scripts)

**Represents:**
- How concepts in a domain relate to each other.

**Example**

- CNN → Backpropagation  
- Backpropagation → Vanishing Gradient  
- Vanishing Gradient → Batch Normalization  

**Role**
- Ensures progressive technical depth  
- Guides the LLM to ask logically connected questions  
- Avoids random or shallow interviews

---

## Key Files

- **build_resume_graph.py** – parses resume and builds Resume KG  
- **concept_expansion.py** – expands skills using Domain KG  
- **project_questions.py** – generates project-specific prompts  
- **generate_questions.py** – LLM interaction  
- **api.py** – FastAPI orchestration  
- **app.py** – Streamlit UI  

---

## How to Run the Project

### 1) Install Dependencies

```bash
pip install -r requirements.txt


2) Start Neo4j
docker run -d --name neo4j \
 -p 7474:7474 -p 7687:7687 \
 -e NEO4J_AUTH=neo4j/password \
 neo4j:5

3) Pull LLM Model
ollama pull mistral


(or a faster model like tinyllama)

4) Build Resume Graph
python resume_graph/build_resume_graph.py

5) Start Backend
uvicorn api:app --reload


API Docs:
http://127.0.0.1:8000/docs

6) Start Frontend
streamlit run app.py

Output

The system returns:

Expanded technical concepts

Skill/theory questions

Project-based questions referring to candidate work