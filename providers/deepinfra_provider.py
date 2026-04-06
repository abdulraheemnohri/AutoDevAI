import requests
from backend.config import DEEPINFRA_API_KEY, API_TIMEOUT

def generate_deepinfra(prompt, model="deepinfra/airoboros-l2-70b-2.1"):
    """Generate response using DeepInfra API."""
    if not DEEPINFRA_API_KEY:
        raise ValueError("DeepInfra API key not found.")

    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
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
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"DeepInfra error: {e}")
        raise
