import re

def extract(text):
    """Extract potential API endpoints from text using regex patterns."""
    # Pattern for common AI API endpoints (OpenAI-compatible, etc.)
    patterns = [
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/chat/completions",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/completions",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/api/generate",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/inference",
        r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9./_-]*)?/v1/models"
    ]
    
    endpoints = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        endpoints.extend(matches)
        
    # Deduplicate
    return list(set(endpoints))
