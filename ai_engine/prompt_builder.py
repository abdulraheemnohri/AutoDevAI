def build_prompt(command, context=""):
    """Builds a detailed prompt based on the command and context."""

    prompts = {
        "review": "Perform a comprehensive code review on the following code. Identify bugs, performance issues, and suggest best practices.",
        "fix": "Suggest an automated fix or refactoring for the following code snippet. Provide the corrected code as well.",
        "explain": "Explain the following code lines, functions, or logic in a clear and concise manner.",
        "summarize": "Generate a summary for the following text (e.g., a commit, pull request, or file content).",
        "optimize": "Analyze the following code and suggest performance or design improvements. Focus on efficiency and readability.",
        "document": "Auto-generate clear and descriptive documentation (e.g., docstrings or comments) for the following code."
    }

    instruction = prompts.get(command, "Please analyze the following content:")

    return f"""
    Command: /ai {command}

    Instructions:
    {instruction}

    Content to process:
    -------------------
    {context}
    -------------------

    Respond in a professional and helpful tone.
    """
