import requests
from backend.config import GROQ_API_KEY, API_TIMEOUT

def generate_groq(prompt, model="llama3-8b-8192"):
    """Generate response using Groq API."""
    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq error: {e}")
        raise
