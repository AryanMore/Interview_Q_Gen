from rag.concept_expansion import expand_concepts
from rag.retrieve import retrieve
from rag.prompt_builder import build_prompt
from llm.generate_questions import generate

skills=["CNN","SQL"]
concepts=expand_concepts()
knowledge=retrieve(concepts)

prompt=build_prompt(skills,concepts,knowledge)
questions=generate(prompt)

print("\nINTERVIEW QUESTIONS:\n",questions)
