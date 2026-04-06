import re

def parse_command(comment_body):
    """Parse AI commands from GitHub comments."""
    # Supported commands: /ai review, /ai fix, /ai explain, /ai summarize, /ai optimize, /ai document
    command_pattern = r"/ai\s+(review|fix|explain|summarize|optimize|document)\s*(.*)"
    match = re.search(command_pattern, comment_body, re.IGNORECASE)
    
    if match:
        command = match.group(1).lower()
        args = match.group(2).strip()
        return command, args
    
    return None, None
