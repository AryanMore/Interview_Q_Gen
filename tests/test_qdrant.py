from rag.retrieve import retrieve

def test_qdrant_retrieval():
    concepts = ["CNN", "Backpropagation"]
    knowledge = retrieve(concepts)

    assert isinstance(knowledge, list)
