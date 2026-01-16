import requests

def generate(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    data = r.json()

    if "response" in data:
        return data["response"]

    if "message" in data:
        raise Exception(data["message"])

    raise Exception(f"Ollama error: {data}")
