from ai_engine.router import generate

def summarize_text(text):
    """Summarizes a given text using an AI model."""
    prompt = f"Please summarize the following text concisely: {text}"
    return generate(prompt)
