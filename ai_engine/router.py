import sqlite3
import requests
import time
from backend.config import DATABASE_PATH, API_TIMEOUT, JULES_API_KEY
from providers.groq_provider import generate_groq
from providers.openrouter_provider import generate_openrouter
from providers.jules_provider import generate_jules
from providers.local_llm_provider import generate_local_llm
from ai_engine.provider_manager import ProviderManager
from ai_engine.agents import get_agent_for_command

def generate(prompt, command=None):
    """Route the prompt to the best available AI provider with agent context."""
    
    manager = ProviderManager(DATABASE_PATH)

    # 1. Add Agent Context if a command is provided
    if command:
        agent = get_agent_for_command(command)
        agent_header = agent.get_prompt_header()
        prompt = f"{agent_header}\n\nUser Task:\n{prompt}"

    # 2. Try hardcoded providers first (if keys exist)
    providers = [
        ("Jules", generate_jules, JULES_API_KEY),
        ("Groq", generate_groq, True),
        ("OpenRouter", generate_openrouter, True),
        ("Local LLM (Ollama)", generate_local_llm, True) # Assumes running if configured
    ]

    for name, func, key_exists in providers:
        if not key_exists:
            continue

        try:
            print(f"🤖 Attempting generation with {name}...")
            start_time = time.time()
            response = func(prompt)
            latency = time.time() - start_time
            print(f"✅ {name} succeeded in {latency:.2f}s.")
            return response
        except Exception as e:
            print(f"⚠️ {name} failed: {e}")
            continue

    # 3. Try discovered APIs from database using ProviderManager
    print("🔍 No hardcoded providers available. Searching database for discovered APIs...")
    active_providers = manager.get_active_providers()

    for provider in active_providers:
        endpoint = provider['endpoint']
        provider_name = provider['name']
        provider_id = provider['id']

        try:
            print(f"🤖 Attempting generation with discovered provider: {provider_name} ({endpoint})...")
            start_time = time.time()
            # Assume OpenAI-compatible for discovered endpoints
            response = requests.post(
                endpoint,
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]},
                timeout=API_TIMEOUT
            )
            latency = time.time() - start_time

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                manager.update_provider_stats(provider_id, success=True, latency=latency)
                print(f"✅ Discovered API {endpoint} succeeded in {latency:.2f}s.")
                return content
            else:
                print(f"⚠️ Discovered API {endpoint} returned status {response.status_code}")
                manager.update_provider_stats(provider_id, success=False, latency=latency)
                if response.status_code in [401, 403, 404]:
                    manager.deactivate_provider(provider_id)
        except Exception as e:
            print(f"⚠️ Discovered API {endpoint} failed: {e}")
            manager.update_provider_stats(provider_id, success=False, latency=API_TIMEOUT)
            continue

    return "❌ Error: No AI provider available. Please check your API keys or wait for discovery to find new endpoints."
