"""Skills-based code generation with mandatory compliance for Manim animations.

Uses dual-model strategy:
- Opus 4.5 for skill selection (complex reasoning/analysis)
- Sonnet for code generation (fast execution)
"""

import logfire

from ..config import settings
from ..llm.client import get_llm_client
from ..prompts import load_prompt
from ..notebook import (
    parse_marimo_notebook,
    build_notebook_context,
    lint_notebook,
    format_issues_for_prompt,
)

# Import skills configuration (will be created)
# For now, use placeholder
try:
    import sys
    from pathlib import Path
    skills_config_path = Path(__file__).parent.parent.parent.parent / "skills_config.py"
    sys.path.insert(0, str(skills_config_path.parent))
    from skills_config import SKILLS

    SKILL_NAME_TO_CONFIG = {
        "core-animation-principles": SKILLS[0] if len(SKILLS) > 0 else None,
        "manim-api-patterns": SKILLS[1] if len(SKILLS) > 1 else None,
        "mathematical-visualization": SKILLS[2] if len(SKILLS) > 2 else None,
        "video-rendering": SKILLS[3] if len(SKILLS) > 3 else None,
        "educational-animation": SKILLS[4] if len(SKILLS) > 4 else None,
        "manimo-notebook": SKILLS[5] if len(SKILLS) > 5 else None,
    }
except ImportError:
    # Placeholder for when skills_config.py doesn't exist yet
    SKILLS = []
    SKILL_NAME_TO_CONFIG = {}


def get_skills_for_request(skill_names: list[str]) -> list[dict]:
    """Get skill configs for requested skill names (max 8)."""
    selected = []
    if "core-animation-principles" in skill_names:
        if SKILL_NAME_TO_CONFIG.get("core-animation-principles"):
            selected.append(SKILL_NAME_TO_CONFIG["core-animation-principles"])
        skill_names = [s for s in skill_names if s != "core-animation-principles"]

    for skill_name in skill_names:
        if len(selected) >= 8:
            break
        if skill_name in SKILL_NAME_TO_CONFIG and SKILL_NAME_TO_CONFIG[skill_name]:
            selected.append(SKILL_NAME_TO_CONFIG[skill_name])

    return selected


async def generate_with_skills(notebook_content: str, user_prompt: str) -> dict:
    """
    Generate Manim animation code using skills-based approach.

    Two-pass approach:
    0. Parse notebook and build context
    1. Analyze task and select relevant skills (LLM call)
    2. Generate code following ALL skill requirements (LLM call)

    Args:
        notebook_content: Current notebook source code
        user_prompt: User's animation request

    Returns:
        dict with keys: patch_type, artifact, rationale, skills_used
    """
    with logfire.span(
        "generation.skills_based",
        user_prompt=user_prompt,
        notebook_length=len(notebook_content),
    ):
        llm = get_llm_client()

        skill_names = [
            "core-animation-principles",
            "manim-api-patterns",
            "mathematical-visualization",
            "video-rendering",
            "educational-animation",
            "manimo-notebook",
        ]

        logfire.info(
            "Using Anthropic Skills API",
            num_skills=len(SKILLS),
            skill_names=skill_names,
        )

        # PASS 0: Parse and Analyze Notebook
        logfire.info("Pass 0: Analyzing notebook structure")
        parse_result = parse_marimo_notebook(notebook_content)
        notebook_context = build_notebook_context(parse_result)
        marimo_issues = lint_notebook(notebook_context, parse_result)

        logfire.info(
            "Notebook context built",
            num_cells=notebook_context.cell_count,
            num_scenes=len(notebook_context.manim_scenes),
            num_issues=len(marimo_issues)
        )

        # PASS 1: Skill Selection
        base_prompt = load_prompt("manim_agent")

        system_prompt_metadata = base_prompt + """

## Available Manim Skills

You have access to the following Manim skills through the Anthropic Skills API:
- core-animation-principles: Timing, easing, scene composition
- manim-api-patterns: Scene, Mobject, Animation classes
- mathematical-visualization: Best practices for math animations
- video-rendering: Optimization, quality settings, formats
- educational-animation: Pedagogical design principles
- manimo-notebook: Marimo notebook patterns for Manim

These skills will be automatically loaded when relevant to your task.
"""

        context_str = notebook_context.to_prompt_context()
        issues_str = format_issues_for_prompt(marimo_issues)

        analysis_message = f"""
<current_notebook>
```python
{notebook_content}
```
</current_notebook>

{context_str}

{issues_str}

<user_request>
{user_prompt}
</user_request>

<task>
Analyze this request and determine which Manim skills are needed.

Consider:
- What scenes/objects are already available?
- What animation techniques does this require?
- Which skills are most relevant?

Respond with a JSON object:
{{
    "skills": ["skill1", "skill2", ...],
    "reasoning": "Why these skills are needed"
}}
</task>
"""

        logfire.info("Pass 1: Skill selection (using Opus for complex reasoning)")
        skill_selection_response = await llm.generate(
            system=system_prompt_metadata,
            user=analysis_message,
            model_override=settings.OPUS_MODEL,
        )

        requested_skills = ["core-animation-principles"]
        if "manim-api-patterns" in skill_selection_response.lower():
            requested_skills.append("manim-api-patterns")
        if "mathematical-visualization" in skill_selection_response.lower():
            requested_skills.append("mathematical-visualization")
        if "video-rendering" in skill_selection_response.lower():
            requested_skills.append("video-rendering")
        if "educational-animation" in skill_selection_response.lower():
            requested_skills.append("educational-animation")
        if "manimo-notebook" in skill_selection_response.lower():
            requested_skills.append("manimo-notebook")

        # PASS 2: Code Generation with Skills
        selected_skills = get_skills_for_request(requested_skills)
        system_prompt_final = base_prompt + """

## Statistical Skills

All Manim skills are available through the Anthropic Skills API.
The skills you identified as relevant will be loaded automatically.

You MUST follow ALL requirements from the loaded skills.
"""

        generation_message = f"""
<current_notebook>
```python
{notebook_content}
```
</current_notebook>

{context_str}

{issues_str}

<user_request>
{user_prompt}
</user_request>

<task>
Generate Manim code following ALL requirements from the loaded skills.
Return a complete @app.cell with your implementation.
</task>
"""

        logfire.info(
            "Pass 2: Generating code with Skills API (using Sonnet for execution)",
            skills_loaded=requested_skills,
        )

        code_response = await llm.generate(
            system=system_prompt_final,
            user=generation_message,
            skills=selected_skills if selected_skills else None,
            model_override=settings.SONNET_MODEL,
        )

        artifact = code_response
        if "```python" in artifact:
            start = artifact.find("```python") + 9
            end = artifact.find("```", start)
            if end > start:
                artifact = artifact[start:end].strip()

        return {
            "patch_type": "cell",
            "artifact": artifact,
            "skills_used": requested_skills,
        }

