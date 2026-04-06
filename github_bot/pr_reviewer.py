import re
from ai_engine.router import generate
from ai_engine.prompt_builder import build_prompt

def review_pull_request(pr_diff):
    """Reviews a pull request using AI and code analysis."""
    
    # 1. Parse the diff to extract changed files and content
    files = parse_diff(pr_diff)
    
    # 2. Build a summary for AI review
    diff_summary = ""
    for filename, content in files.items():
        diff_summary += f"File: {filename}\nContent:\n{content}\n\n"

    # 3. Request AI review using the prompt builder
    prompt = build_prompt("review", diff_summary)
    ai_review = generate(prompt)

    response = f"### 🤖 AI Code Review:\n\n{ai_review}\n\n"
    
    return response

def parse_diff(pr_diff):
    """Simple diff parser to extract changed files and their approximate content."""
    files = {}
    current_file = None
    current_content = []

    for line in pr_diff.splitlines():
        # Match 'diff --git a/file1 b/file2'
        match = re.match(r'^diff --git a/(.+) b/(.+)', line)
        if match:
            if current_file:
                files[current_file] = "\n".join(current_content)
            current_file = match.group(2)
            current_content = []
            continue

        # Extract lines starting with '+' (additions) or ' ' (context)
        # Skip '+++' or '---' lines
        if line.startswith('+++') or line.startswith('---'):
            continue
        if line.startswith('+') or line.startswith(' '):
            current_content.append(line[1:])

    if current_file:
        files[current_file] = "\n".join(current_content)

    return files
