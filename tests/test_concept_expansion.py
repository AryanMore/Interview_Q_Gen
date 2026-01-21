from rag.concept_expansion import expand_concepts

def test_concept_expansion_not_empty():
    concepts = expand_concepts()
    assert isinstance(concepts, list)
