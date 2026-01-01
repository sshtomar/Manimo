"""Utility functions."""

import random
import uuid


def generate_notebook_name() -> str:
    """Generate a memorable notebook ID like 'untitled-yellow-landfowl'."""
    adjectives = [
        "yellow", "blue", "green", "red", "purple", "orange", "pink", "cyan",
        "bright", "dark", "light", "vivid", "muted", "bold", "soft",
        "swift", "calm", "bold", "gentle", "sharp", "smooth", "quick",
    ]
    nouns = [
        "landfowl", "seabird", "songbird", "raptor", "waterfowl", "parrot",
        "penguin", "flamingo", "eagle", "hawk", "owl", "crow", "robin",
        "sparrow", "finch", "wren", "thrush", "lark", "swallow", "martin",
    ]
    return f"untitled-{random.choice(adjectives)}-{random.choice(nouns)}"


def generate_notebook_title(notebook_id: str) -> str:
    """Generate a display title from notebook ID."""
    # Convert "untitled-yellow-landfowl" -> "Untitled Yellow Landfowl"
    parts = notebook_id.replace("untitled-", "").split("-")
    title_parts = [part.capitalize() for part in parts]
    return " ".join(title_parts)

