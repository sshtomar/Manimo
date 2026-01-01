"""Orchestrates skills-based code generation workflow."""

import logfire
from ..models.requests import AskAIResponse
from ..storage.r2 import get_notebook_content

# Skills-based generation with 2-pass approach
from .skills_generator import generate_with_skills


async def orchestrate_generation(
    notebook_id: str,
    user_id: str,
    user_prompt: str,
    apply: bool = False,
) -> AskAIResponse:
    """
    Orchestrate skills-based code generation.

    Two-pass approach:
    - Pass 1: Analyze task and select relevant skills (LLM call)
    - Pass 2: Generate code following ALL skill requirements (LLM call)

    Skills encode quality standards and mandatory compliance ensures rigor.

    Args:
        notebook_id: ID of the notebook to modify
        user_id: User ID for storage
        user_prompt: User's animation request
        apply: Whether to apply the patch automatically

    Returns:
        AskAIResponse with final artifact and metadata
    """
    with logfire.span(
        "orchestrator.skills_based_generation",
        notebook_id=notebook_id,
        user_id=user_id,
        user_prompt=user_prompt,
    ):
        # 1. Load notebook content
        notebook_content = await get_notebook_content(notebook_id, user_id)

        # 2. Generate code using skills (2-pass: skill selection → code generation)
        print(f"[Skills Generator] Generating animation code with skills...")
        result = await generate_with_skills(
            notebook_content=notebook_content,
            user_prompt=user_prompt,
        )

        # 3. Optionally apply
        applied_version_key = None
        if apply:
            from ..storage.r2 import save_notebook_content
            applied_version_key = await save_notebook_content(
                notebook_id, user_id, result["artifact"]
            )

        # 4. Build response
        rationale = f"Skills-based generation: {', '.join(result['skills_used'])}"

        logfire.info(
            "Skills-based generation complete",
            skills_used=result["skills_used"],
            artifact_length=len(result["artifact"]),
        )

        print(f"Code generated using {len(result['skills_used'])} skills")

        return AskAIResponse(
            patch_type=result["patch_type"],
            artifact=result["artifact"],
            rationale=rationale,
            applied_version_key=applied_version_key,
            discussion_history=None,
        )

