import spacy, pdfplumber, re

nlp = spacy.load("en_core_web_sm")

SKILLS = ["python","tensorflow","cnn","sql","opencv","pytorch","fastapi"]

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([p.extract_text() or "" for p in pdf.pages])

def extract_entities(text):
    skills, projects = set(), []

    for s in SKILLS:
        if re.search(rf"\b{s}\b", text.lower()):
            skills.add(s.capitalize())

    for line in text.split("\n"):
        if len(line.split()) > 4 and "project" not in line.lower():
            projects.append(line.strip())

    return list(skills), projects

if __name__ == "__main__":
    text = extract_text("resume.pdf")
    skills, projects = extract_entities(text)
    print(skills)
    print(projects[:3])
