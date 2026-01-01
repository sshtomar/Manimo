"""Parse Marimo notebook source code."""

import ast
import re
from dataclasses import dataclass
from typing import List


@dataclass
class NotebookParseResult:
    """Result of parsing a Marimo notebook."""
    cells: List[dict]  # List of cell dicts with 'code', 'name', 'decorator'
    imports: List[str]  # List of imported modules
    classes: List[str]  # List of class names
    functions: List[str]  # List of function names


def parse_marimo_notebook(source: str) -> NotebookParseResult:
    """Parse a Marimo notebook source file."""
    cells = []
    imports = []
    classes = []
    functions = []

    # Split by @app.cell decorator
    cell_pattern = r'@app\.cell\s*\n\s*def\s+(\w+)'
    matches = list(re.finditer(cell_pattern, source))

    for i, match in enumerate(matches):
        cell_name = match.group(1)
        start = match.start()

        # Find end of cell (next @app.cell or end of file)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(source)

        cell_code = source[start:end]
        cells.append({
            "name": cell_name,
            "code": cell_code,
            "decorator": "@app.cell",
        })

        # Parse AST to extract imports, classes, functions
        try:
            tree = ast.parse(cell_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
        except SyntaxError:
            pass

    return NotebookParseResult(
        cells=cells,
        imports=list(set(imports)),
        classes=list(set(classes)),
        functions=list(set(functions)),
    )

