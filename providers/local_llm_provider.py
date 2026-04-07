import requests
import json
from backend.config import API_TIMEOUT

# Default Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_local_llm(prompt, model="llama3"):
    """Generate response using a local Ollama instance."""

    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    }

    try:
        # We use a shorter timeout for local models if they are not running
        response = requests.post(OLLAMA_URL, json=data, timeout=5)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response content.")
    except requests.exceptions.ConnectionError:
        print("⚠️ Ollama is not running on localhost:11434.")
        raise ConnectionError("Ollama instance not found.")
    except Exception as e:
        print(f"Local LLM error: {e}")
        raise
