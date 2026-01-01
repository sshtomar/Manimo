"""Build notebook context for agent prompts."""

from dataclasses import dataclass
from typing import List
from .parser import NotebookParseResult


@dataclass
class NotebookContext:
    """Context extracted from notebook."""
    cell_count: int
    variable_names: List[str]
    dataframe_names: List[str]
    class_names: List[str]
    function_names: List[str]
    imports: List[str]
    manim_scenes: List[str]  # List of Scene class names

    def to_prompt_context(self) -> str:
        """Convert to prompt-friendly string."""
        lines = [
            f"**Notebook Structure:**",
            f"- {self.cell_count} cells",
            f"- Imports: {', '.join(self.imports) if self.imports else 'None'}",
        ]

        if self.manim_scenes:
            lines.append(f"- Manim Scenes: {', '.join(self.manim_scenes)}")

        if self.class_names:
            lines.append(f"- Classes: {', '.join(self.class_names)}")

        if self.function_names:
            lines.append(f"- Functions: {', '.join(self.function_names)}")

        return "\n".join(lines)


def build_notebook_context(parse_result: NotebookParseResult) -> NotebookContext:
    """Build context from parse result."""
    # Extract Manim Scene classes
    manim_scenes = [cls for cls in parse_result.classes if "Scene" in cls or cls.endswith("Scene")]

    return NotebookContext(
        cell_count=len(parse_result.cells),
        variable_names=[],  # Would need more sophisticated parsing
        dataframe_names=[],  # Would need more sophisticated parsing
        class_names=parse_result.classes,
        function_names=parse_result.functions,
        imports=parse_result.imports,
        manim_scenes=manim_scenes,
    )

