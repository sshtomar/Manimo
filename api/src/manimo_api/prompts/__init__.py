"""Prompt loading utilities."""

from pathlib import Path


def load_prompt(name: str) -> str:
    """Load a prompt template by name."""
    prompt_file = Path(__file__).parent / f"{name}.txt"
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt not found: {name}")
    return prompt_file.read_text()

