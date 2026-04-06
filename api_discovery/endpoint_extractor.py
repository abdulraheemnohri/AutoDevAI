import re

def extract(text):
    """Extract potential API endpoints from text using expanded regex patterns."""
    # Pattern for common AI API endpoints (OpenAI-compatible, etc.)
    patterns = [
        # OpenAI compatible completions
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/chat/completions",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/completions",

        # DeepInfra and similar
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/inference",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/models",

        # Together AI and similar
        r"https?://api\.[a-zA-Z0-9.-]+\.com/v1/completions",

        # Local LLM APIs (Ollama, LM Studio)
        r"https?://[a-zA-Z0-9.-]+(?::[0-9]+)?/api/generate",
        r"https?://[a-zA-Z0-9.-]+(?::[0-9]+)?/api/chat",

        # General pattern for AI-like URLs
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/ai/(?:v[0-9]+/)?completions",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/api/(?:v[0-9]+/)?generate"
    ]
    
    endpoints = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        endpoints.extend(matches)
        
    # Deduplicate and return
    return list(set(endpoints))
