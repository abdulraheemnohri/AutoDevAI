import ast
import os

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
        # Check for bare 'except:'
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(f"Line {node.lineno}: Bare 'except:' clause found. Use specific exceptions.")
            
        # Check for 'eval()'
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
            issues.append(f"Line {node.lineno}: Use of 'eval()' detected. This is a security risk.")
            
        # Check for 'print()' (suggest logging)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            issues.append(f"Line {node.lineno}: 'print()' used. Consider using a logger.")

        # Check for function complexity (too many arguments)
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > 5:
                issues.append(f"Line {node.lineno}: Function '{node.name}' has too many arguments ({len(node.args.args)}). Consider refactoring.")

        # Check for overly complex functions (rough estimation by node count)
        if isinstance(node, ast.FunctionDef):
            node_count = sum(1 for _ in ast.walk(node))
            if node_count > 100:
                issues.append(f"Line {node.lineno}: Function '{node.name}' is too complex (node count: {node_count}). Consider splitting it.")

    return issues

def analyze_repository(repo_path):
    """Analyze all Python files in a repository."""
    all_issues = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                issues = analyze_python_file(file_path)
                if issues:
                    all_issues[file_path] = issues
    return all_issues
