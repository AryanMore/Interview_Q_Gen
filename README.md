# Context-Aware Interview Question Generator

This system generates intelligent interview questions from a candidate resume using a combination of:

- Resume Knowledge Graph (Neo4j)  
- Domain Knowledge Graph  
- Vector RAG (Qdrant)  
- Local LLM (Ollama)  
- Streamlit UI + FastAPI backend  

The goal is to produce **role-specific, project-aware and progressive interview questions** instead of generic LLM outputs.

---

## Project Workflow

1. **Resume Upload**
   - Recruiter uploads a PDF resume and selects target role.

2. **Resume Parsing**
   - Text is extracted using pdfplumber.
   - Skills are detected using a curated skills catalog.
   - Project descriptions are identified from resume lines.

3. **Resume Knowledge Graph Creation**
   - Nodes: Candidate, Skill, Project  
   - Relations:
     - Candidate ──HAS_SKILL──▶ Skill  
     - Candidate ──WORKED_ON──▶ Project  
     - Project ──USES──▶ Skill  

4. **Concept Expansion**
   - Detected skills are mapped to the Domain Knowledge Graph.
   - Related technical concepts are expanded (e.g., CNN → Backprop → Vanishing Gradient).

5. **RAG Retrieval**
   - Expanded concepts are used to retrieve interviewer knowledge from Qdrant.

6. **LLM Generation**
   - Two types of questions are generated:
     - Skill/Theory questions  
     - Project-specific questions grounded in candidate experience.

7. **Frontend Display**
   - Streamlit shows:
     - Expanded concepts  
     - Skill questions  
     - Project questions

---

## Two Knowledge Graphs – Why & How

### 1) Resume Knowledge Graph (Dynamic)

**Purpose:**  
Represents facts specific to the candidate.

**Created From:**  
`resume_graph/build_resume_graph.py`

**Structure**

- Candidate nodes  
- Skill nodes (from curated catalog)  
- Project nodes (from resume text)

**Relations**

- HAS_SKILL  
- WORKED_ON  
- USES (project → skill via semantic similarity)

**Role in System**

- Grounds the system to the candidate’s real experience  
- Enables project-aware questioning  
- Prevents hallucinated skills

---

### 2) Domain Knowledge Graph (Static)

**Purpose:**  
Represents how the technical domain itself is structured.

**Defined In:**  
`domain_graph/seeds.yaml` (or loader scripts)

**Example Relations**

- CNN ──HAS_CONCEPT──▶ Backpropagation  
- Backpropagation ──CAUSES──▶ Vanishing Gradient  
- Vanishing Gradient ──MITIGATED_BY──▶ BatchNorm  

**Role in System**

- Provides concept progression  
- Ensures questions follow real technical dependencies  
- Makes interviews deeper instead of keyword-based

---

## Key Files Explained

- **build_resume_graph.py** – parses resume and builds Resume KG  
- **concept_expansion.py** – queries Domain KG to expand skills  
- **retrieve.py** – fetches interview knowledge from Qdrant  
- **project_questions.py** – generates project-specific prompts  
- **api.py** – FastAPI orchestration  
- **app.py** – Streamlit interface  

---

## How to Run the Project

### 1) Install Dependencies

```bash
pip install -r requirements.txt
