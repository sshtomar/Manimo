"""Autonomous orchestrator using Claude Agent SDK.

Unlike the standard orchestrator that makes LLM calls and returns text,
this orchestrator uses the Agent SDK running in a Modal sandbox to:
1. Read and understand the notebook
2. Generate appropriate Manim code
3. Optionally verify by running manim
4. Iterate on errors if needed

The agent runs in an isolated Modal container for security.
"""

import modal
import logfire

from ..models.requests import AskAIResponse
from ..storage.r2 import save_notebook_content
from ..config import settings


async def orchestrate_with_agent(
    notebook_id: str,
    user_id: str,
    user_prompt: str,
    apply: bool = False,
    use_subagents: bool = False,
) -> AskAIResponse:
    """Orchestrate code generation using Claude Agent SDK in Modal sandbox.

    The agent runs in an isolated Modal container where it can safely
    use tools like Read, Glob, Grep, and Bash without affecting the
    API server.

    Args:
        notebook_id: ID of the notebook to modify
        user_id: User ID for storage
        user_prompt: User's animation request
        apply: Whether to apply the patch automatically
        use_subagents: Use dual-agent (planner + coder) approach

    Returns:
        AskAIResponse with final artifact and metadata
    """
    with logfire.span(
        "orchestrator.agent_mode",
        notebook_id=notebook_id,
        user_id=user_id,
        user_prompt=user_prompt,
        use_subagents=use_subagents,
    ):
        logfire.info(
            "Starting agent generation in Modal sandbox",
            mode="subagents" if use_subagents else "single",
        )

        # Call the Modal sandbox function remotely
        run_agent = modal.Function.from_name(
            "manimo-notebooks", "run_agent_in_sandbox"
        )

        result = run_agent.remote(
            notebook_id=notebook_id,
            user_id=user_id,
            user_prompt=user_prompt,
            use_subagents=use_subagents,
            model=settings.SONNET_MODEL,
            opus_model=settings.OPUS_MODEL,
        )

        applied_version_key = None
        if apply and result["artifact"]:
            applied_version_key = await save_notebook_content(
                notebook_id, user_id, result["artifact"]
            )

        mode_desc = "dual-agent (planner+coder)" if use_subagents else "single agent"
        rationale = f"Agent SDK generation ({mode_desc}) [Modal sandbox]"

        if result.get("session_id"):
            rationale += f" [session: {result['session_id'][:8]}...]"

        logfire.info(
            "Agent generation complete",
            artifact_length=len(result["artifact"]),
            session_id=result.get("session_id"),
        )

        return AskAIResponse(
            patch_type=result["patch_type"],
            artifact=result["artifact"],
            rationale=rationale,
            applied_version_key=applied_version_key,
            discussion_history=None,
        )
