"""Autonomous orchestrator using Claude Agent SDK.

Unlike the standard orchestrator that makes LLM calls and returns text,
this orchestrator uses the Agent SDK to autonomously:
1. Read and understand the notebook
2. Generate appropriate Manim code
3. Optionally verify by running manim
4. Iterate on errors if needed
"""

import tempfile
from pathlib import Path

import logfire

from ..models.requests import AskAIResponse
from ..storage.r2 import get_notebook_content, save_notebook_content
from .agent_generator import collect_agent_result, AGENT_SDK_AVAILABLE


async def orchestrate_with_agent(
    notebook_id: str,
    user_id: str,
    user_prompt: str,
    apply: bool = False,
    use_subagents: bool = False,
) -> AskAIResponse:
    """Orchestrate code generation using Claude Agent SDK.

    The agent autonomously reads files, generates code, and can
    optionally verify the output. This is more powerful than the
    standard approach but requires the Agent SDK.

    Args:
        notebook_id: ID of the notebook to modify
        user_id: User ID for storage
        user_prompt: User's animation request
        apply: Whether to apply the patch automatically
        use_subagents: Use dual-agent (planner + coder) approach

    Returns:
        AskAIResponse with final artifact and metadata
    """
    if not AGENT_SDK_AVAILABLE:
        raise RuntimeError(
            "Agent SDK not available. Install with: pip install claude-agent-sdk"
        )

    with logfire.span(
        "orchestrator.agent_mode",
        notebook_id=notebook_id,
        user_id=user_id,
        user_prompt=user_prompt,
        use_subagents=use_subagents,
    ):
        notebook_content = await get_notebook_content(notebook_id, user_id)

        with tempfile.TemporaryDirectory() as tmpdir:
            notebook_path = Path(tmpdir) / "notebook.py"
            notebook_path.write_text(notebook_content)

            logfire.info(
                "Starting agent generation",
                mode="subagents" if use_subagents else "single",
            )

            result = await collect_agent_result(
                notebook_path=str(notebook_path),
                user_prompt=user_prompt,
                use_subagents=use_subagents,
            )

        applied_version_key = None
        if apply and result["artifact"]:
            applied_version_key = await save_notebook_content(
                notebook_id, user_id, result["artifact"]
            )

        mode_desc = "dual-agent (planner+coder)" if use_subagents else "single agent"
        rationale = f"Agent SDK generation ({mode_desc})"

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
