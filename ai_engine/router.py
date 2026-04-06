import sqlite3
import requests
from backend.config import DATABASE_PATH, API_TIMEOUT
from providers.groq_provider import generate_groq
from providers.openrouter_provider import generate_openrouter

def generate(prompt):
    """Route the prompt to the best available AI provider."""
    
    # 1. Try hardcoded providers first (if keys exist)
    providers = [
        ("Groq", generate_groq),
        ("OpenRouter", generate_openrouter)
    ]

    for name, func in providers:
        try:
            print(f"🤖 Attempting generation with {name}...")
            return func(prompt)
        except Exception as e:
            print(f"⚠️ {name} failed: {e}")
            continue

    # 2. Try discovered APIs from database
    print("🔍 No hardcoded providers available. Searching database for discovered APIs...")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("SELECT endpoint, provider FROM apis WHERE status='active' ORDER BY success_rate DESC, latency ASC")
        discovered_apis = c.fetchall()
        conn.close()

        for endpoint, provider_name in discovered_apis:
            try:
                print(f"🤖 Attempting generation with discovered provider: {provider_name} ({endpoint})...")
                # Assume OpenAI-compatible for discovered endpoints
                response = requests.post(
                    endpoint,
                    json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]},
                    timeout=API_TIMEOUT
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"⚠️ Discovered API {endpoint} failed: {e}")
                continue
    except Exception as e:
        print(f"❌ Database error: {e}")

    return "❌ Error: No AI provider available. Please check your API keys or wait for discovery to find new endpoints."
