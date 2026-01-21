import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate(prompt: str) -> str:
    r = requests.post(f"{os.getenv('OLLAMA_URL')}/api/generate", json={
        "model": os.getenv("OLLAMA_MODEL", "mistral"),
        "prompt": prompt,
        "stream": False
    })

    data = r.json()

    if "response" in data:
        return data["response"]

    if "message" in data:
        raise Exception(data["message"])

    raise Exception(f"Ollama error: {data}")
