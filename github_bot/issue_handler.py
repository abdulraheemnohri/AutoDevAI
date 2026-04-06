from ai_engine.router import generate

def handle_issue_comment(comment_body):
    """Handles AI commands in issue comments."""
    # This is a simplified example. In a real scenario, you would parse commands
    # and trigger appropriate AI actions.
    if "/ai summarize" in comment_body:
        return generate(f"Summarize the following issue comment: {comment_body}")
    return ""
