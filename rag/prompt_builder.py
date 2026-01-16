def build_prompt(skills, concepts, knowledge_chunks):
    return f"""
You are a senior technical interviewer.

Candidate Skills: {', '.join(skills)}
Expanded Concepts: {', '.join(concepts)}

Reference Knowledge:
{chr(10).join('- '+k for k in knowledge_chunks)}

Generate 5 interview questions:
- 3 technical
- 1 scenario based
- 1 behavioral
Ensure increasing difficulty.
Avoid repeating reference knowledge verbatim.
"""
