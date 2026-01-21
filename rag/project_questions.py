from llm.generate_questions import generate
from rag.concept_expansion import expand_concepts

def project_prompt(project_text, skills):

    prompt = f"""
You are a senior technical interviewer.

The candidate has worked on the following projects:

{project_text}

Generate interview questions that:

1. Refer explicitly to these projects  
2. Cover:
   - design decisions  
   - implementation details  
   - challenges faced  
   - impact/outcomes  

Do NOT ask generic theory questions.
Group questions per project if possible.
"""

    return generate(prompt)
