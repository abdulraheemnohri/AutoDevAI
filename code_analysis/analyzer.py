import ast
import os
import re

def analyze_python_file(file_path):
    """Analyze a Python file for potential issues using AST."""
    print(f"🔬 Analyzing Python file: {file_path}")
    
    if not os.path.exists(file_path):
        return [f"Error: File {file_path} not found."]

    with open(file_path, "r") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError as e:
            return [f"Syntax error in {file_path}: {e}"]

    issues = []
    
    for node in ast.walk(tree):
        # Python-specific AST checks
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(f"Line {node.lineno}: Bare 'except:' clause found.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
            issues.append(f"Line {node.lineno}: Use of 'eval()' detected.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            issues.append(f"Line {node.lineno}: 'print()' used. Consider logging.")
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > 5:
                issues.append(f"Line {node.lineno}: Function '{node.name}' has too many arguments.")

    return issues

def analyze_js_ts_file(file_path):
    """Analyze a JavaScript/TypeScript file using regex patterns."""
    print(f"🔬 Analyzing JS/TS file: {file_path}")

    if not os.path.exists(file_path):
        return [f"Error: File {file_path} not found."]

    issues = []
    try:
        with open(file_path, "r", errors="ignore") as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                line_no = i + 1
                # 1. Use of 'console.log'
                if "console.log(" in line:
                    issues.append(f"Line {line_no}: 'console.log' used. Consider a production logger.")
                # 2. Use of 'eval'
                if "eval(" in line:
                    issues.append(f"Line {line_no}: 'eval()' detected. This is a security risk.")
                # 3. Use of 'var' instead of 'let' or 'const'
                if re.search(r'\bvar\b', line):
                    issues.append(f"Line {line_no}: 'var' keyword used. Consider using 'let' or 'const'.")
                # 4. Potentially dangerous innerHTML
                if ".innerHTML =" in line:
                    issues.append(f"Line {line_no}: Use of '.innerHTML' detected. Consider '.textContent' or sanitized alternatives to prevent XSS.")

    except Exception as e:
        issues.append(f"Error reading file: {e}")

    return issues

def analyze_repository(repo_path):
    """Analyze all supported files in a repository."""
    all_issues = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".py"):
                issues = analyze_python_file(file_path)
            elif file.endswith((".js", ".ts")):
                issues = analyze_js_ts_file(file_path)
            else:
                continue

            if issues:
                all_issues[file_path] = issues
    return all_issues
