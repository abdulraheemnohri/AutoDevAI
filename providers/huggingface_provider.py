import requests
from backend.config import HF_TOKEN, API_TIMEOUT

def generate_huggingface(prompt, model="HuggingFaceH4/zephyr-7b-beta"):
    """Generate response using HuggingFace Inference API."""
    if not HF_TOKEN:
        raise ValueError("HuggingFace token not found.")

    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    try:
        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 100}
        }, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        print(f"HuggingFace error: {e}")
        raise
