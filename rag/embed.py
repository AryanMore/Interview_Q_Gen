from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

def embed(text: str):
    return model.encode(text)
