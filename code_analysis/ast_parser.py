# Placeholder for advanced AST parsing functions

def get_function_definitions(tree):
    """Extracts function definitions from an AST."""
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return functions
