"""Model selection logic for dual-model strategy.

Opus 4.5 handles planning, analysis, and complex reasoning.
Sonnet handles execution requests and vision-based verification.
"""

import re
from enum import Enum


class TaskType(Enum):
    """Types of tasks that determine model selection."""

    PLANNING = "planning"
    EXECUTION = "execution"
    VERIFICATION = "verification"


OPUS_PATTERNS = [
    r"\?",  # Questions
    r"\bhow\b",
    r"\bwhat\b",
    r"\bwhy\b",
    r"\bdesign\b",
    r"\bplan\b",
    r"\bsuggest\b",
    r"\bbest practice\b",
    r"\banalyze\b",
    r"\bexplain\b",
    r"\bcompare\b",
    r"\bevaluate\b",
    r"\barchitect\b",
]

SONNET_PATTERNS = [
    r"\badd\b",
    r"\bcreate\b",
    r"\bconnect\b",
    r"\bremove\b",
    r"\bupdate\b",
    r"\bmove\b",
    r"\bgenerate\b",
    r"\bimplement\b",
    r"\bwrite\b",
    r"\bbuild\b",
    r"\bfix\b",
    r"\bchange\b",
]


def select_task_type(instruction: str, has_existing_content: bool = False) -> TaskType:
    """Auto-select task type based on instruction patterns.

    Args:
        instruction: The user instruction/prompt
        has_existing_content: Whether there's existing content to modify

    Returns:
        TaskType indicating which model class to use
    """
    instruction_lower = instruction.lower()

    # Check for Opus patterns first (planning takes priority for questions)
    for pattern in OPUS_PATTERNS:
        if re.search(pattern, instruction_lower):
            return TaskType.PLANNING

    # Check for execution patterns
    for pattern in SONNET_PATTERNS:
        if re.search(pattern, instruction_lower):
            return TaskType.EXECUTION

    # Default: if has existing content, assume modification (Sonnet)
    # Otherwise, assume new design/planning (Opus)
    return TaskType.EXECUTION if has_existing_content else TaskType.PLANNING
