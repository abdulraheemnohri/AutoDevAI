import re
import os

def scan_for_security_issues(code_content):
    """Scans code for common security vulnerabilities using regex."""
    issues = []

    # 1. Potential command injection
    if "os.system(" in code_content or "subprocess.Popen(shell=True" in code_content:
        issues.append("Potential command injection vulnerability: Avoid shell=True or os.system().")

    # 2. Potential hardcoded secrets (API keys, passwords)
    # Simple regex for common secret patterns
    secret_patterns = [
        (r"(?:api_key|secret|password|token)\s*=\s*['\"][a-zA-Z0-9_\-\.]{10,}['\"]", "Possible hardcoded secret (API key, password, or token) detected."),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token detected."),
        (r"sk-[a-zA-Z0-9]{48}", "OpenAI API key detected.")
    ]

    for pattern, message in secret_patterns:
        matches = re.finditer(pattern, code_content, re.IGNORECASE)
        for match in matches:
            line_no = code_content.count('\n', 0, match.start()) + 1
            issues.append(f"Line {line_no}: {message}")

    return issues

def scan_repository_for_security(repo_path):
    """Scan all files in a repository for security issues."""
    all_issues = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".env", ".yaml", ".yml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        issues = scan_for_security_issues(content)
                        if issues:
                            all_issues[file_path] = issues
                except Exception as e:
                    print(f"⚠️ Could not scan {file_path}: {e}")

    return all_issues
