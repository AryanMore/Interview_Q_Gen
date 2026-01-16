from llm.generate_questions import generate
from rag.concept_expansion import expand_concepts

def project_prompt(project, skills):

    concepts = expand_concepts()

    prompt = f"""
You are a senior interviewer.

Project Description:
{project}

Skills Inferred: {', '.join(skills)}

Generate 6 interview questions:

1-2: Architecture & Design  
3-4: Implementation details  
5: Debugging challenge  
6: Business impact

Make questions specific to THIS project.
"""

    return generate(prompt)
