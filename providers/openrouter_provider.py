import requests
from backend.config import OPENROUTER_API_KEY, API_TIMEOUT

def generate_openrouter(prompt, model="openai/gpt-3.5-turbo"):
    """Generate response using OpenRouter API."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key not found.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
        print(f"OpenRouter error: {e}")
        raise
