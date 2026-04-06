# Placeholder for security scanning logic

def scan_for_security_issues(code_content):
    """Scans code for common security vulnerabilities."""
    issues = []
    if "os.system(" in code_content:
        issues.append("Potential command injection vulnerability: os.system() detected.")
    return issues
