"""Lint Marimo notebooks for common issues."""

from dataclasses import dataclass
from typing import List
from .context import NotebookContext
from .parser import NotebookParseResult


@dataclass
class NotebookIssue:
    """A linting issue found in the notebook."""
    severity: str  # "error" | "warning" | "info"
    message: str
    cell_name: str | None = None


def lint_notebook(context: NotebookContext, parse_result: NotebookParseResult) -> List[NotebookIssue]:
    """Lint notebook for common Manim/Marimo issues."""
    issues = []

    # Check for Manim import
    has_manim = any("manim" in imp.lower() for imp in context.imports)
    if not has_manim and context.cell_count > 1:
        issues.append(NotebookIssue(
            severity="warning",
            message="No Manim import found. Add 'from manim import *' to use Manim features.",
        ))

    # Check for Scene classes
    if not context.manim_scenes and context.cell_count > 2:
        issues.append(NotebookIssue(
            severity="info",
            message="No Manim Scene classes found. Create a Scene class to render animations.",
        ))

    return issues


def format_issues_for_prompt(issues: List[NotebookIssue]) -> str:
    """Format issues for inclusion in prompt."""
    if not issues:
        return ""

    lines = ["**Notebook Issues:**"]
    for issue in issues:
        lines.append(f"- [{issue.severity.upper()}] {issue.message}")

    return "\n".join(lines)

