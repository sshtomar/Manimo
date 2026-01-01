"""Agent-based Manim code generation using Claude Agent SDK.

Uses Claude Agent SDK for autonomous code generation with built-in
tool execution. The agent can read files, generate code, run manim
to verify, and iterate on errors.
"""

import asyncio
from pathlib import Path
from typing import AsyncIterator

import logfire

try:
    from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
    AGENT_SDK_AVAILABLE = True
except ImportError:
    AGENT_SDK_AVAILABLE = False

from ..config import settings


MANIM_AGENT_SYSTEM = """You are an expert Manim animation developer. Your task is to
create high-quality mathematical animations using Manim for Marimo notebooks.

When generating Manim code:
1. Always use proper Scene class structure with construct() method
2. Include clear comments explaining the animation approach
3. Use appropriate timing (run_time) for animations
4. Follow mathematical visualization best practices
5. Return code as a complete @app.cell block for Marimo

For mathematical visualizations:
- Use linear rate_func for differential equations and time-dependent processes
- Always label axes and important elements with MathTex
- Maintain mathematical accuracy over visual appeal

Output format: Return a complete @app.cell with the Scene class."""


async def generate_with_agent(
    notebook_path: str,
    user_prompt: str,
    working_dir: str | None = None,
    verify_with_manim: bool = False,
) -> AsyncIterator[dict]:
    """Generate Manim code using Claude Agent SDK.

    The agent autonomously reads the notebook, generates code, and
    optionally verifies it by running manim.

    Args:
        notebook_path: Path to the Marimo notebook file
        user_prompt: User's animation request
        working_dir: Working directory for the agent
        verify_with_manim: Whether to run manim to verify the code

    Yields:
        dict messages from the agent with progress and results
    """
    if not AGENT_SDK_AVAILABLE:
        raise RuntimeError("claude-agent-sdk not installed")

    tools = ["Read", "Glob", "Grep"]
    if verify_with_manim:
        tools.append("Bash")

    full_prompt = f"""Read the notebook at {notebook_path} and understand its structure.

User request: {user_prompt}

Generate a new @app.cell block with Manim code that fulfills this request.
Follow all Manim best practices for mathematical animations.

{"After generating the code, verify it by running: python -c 'exec(open(\"temp_scene.py\").read())' to check for syntax errors." if verify_with_manim else ""}

Return the complete @app.cell code block."""

    with logfire.span(
        "agent.generate_manim",
        notebook_path=notebook_path,
        user_prompt=user_prompt,
        verify=verify_with_manim,
    ):
        async for message in query(
            prompt=full_prompt,
            options=ClaudeAgentOptions(
                system_prompt=MANIM_AGENT_SYSTEM,
                allowed_tools=tools,
                cwd=working_dir or str(Path(notebook_path).parent),
                model=settings.SONNET_MODEL,
            )
        ):
            yield _convert_message(message)


async def generate_with_subagents(
    notebook_path: str,
    user_prompt: str,
    working_dir: str | None = None,
) -> AsyncIterator[dict]:
    """Generate Manim code using specialized subagents.

    Uses a dual-agent approach:
    - Planner agent (Opus): Analyzes requirements and designs approach
    - Coder agent (Sonnet): Implements the animation code

    Args:
        notebook_path: Path to the Marimo notebook file
        user_prompt: User's animation request
        working_dir: Working directory for the agent

    Yields:
        dict messages from the agents with progress and results
    """
    if not AGENT_SDK_AVAILABLE:
        raise RuntimeError("claude-agent-sdk not installed")

    full_prompt = f"""Analyze the notebook at {notebook_path} and the user's request.

User request: {user_prompt}

First, use the manim-planner agent to design the animation approach.
Then, use the manim-coder agent to implement the code.

Return the final @app.cell code block."""

    with logfire.span(
        "agent.generate_with_subagents",
        notebook_path=notebook_path,
        user_prompt=user_prompt,
    ):
        async for message in query(
            prompt=full_prompt,
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Glob", "Grep", "Task"],
                cwd=working_dir or str(Path(notebook_path).parent),
                agents={
                    "manim-planner": AgentDefinition(
                        description="Plans Manim animation structure and approach",
                        prompt="""You are a Manim animation architect. Analyze the request and:
1. Identify the mathematical concepts to visualize
2. Choose appropriate Manim objects and animations
3. Plan the timing and scene structure
4. List any potential issues or edge cases

Return a structured plan, not code.""",
                        tools=["Read", "Glob", "Grep"],
                        model=settings.OPUS_MODEL,
                    ),
                    "manim-coder": AgentDefinition(
                        description="Implements Manim animation code",
                        prompt="""You are a Manim code implementer. Given a plan:
1. Write clean, well-commented Manim code
2. Use proper Scene class structure
3. Follow all timing and animation best practices
4. Return a complete @app.cell block

Focus on implementation quality and correctness.""",
                        tools=["Read", "Glob", "Grep"],
                        model=settings.SONNET_MODEL,
                    ),
                }
            )
        ):
            yield _convert_message(message)


def _convert_message(message) -> dict:
    """Convert Agent SDK message to dict format."""
    result = {"type": getattr(message, "type", "unknown")}

    if hasattr(message, "subtype"):
        result["subtype"] = message.subtype

    if hasattr(message, "result"):
        result["result"] = message.result

    if hasattr(message, "content"):
        result["content"] = message.content

    if hasattr(message, "tool_name"):
        result["tool_name"] = message.tool_name

    if hasattr(message, "tool_input"):
        result["tool_input"] = message.tool_input

    if hasattr(message, "session_id"):
        result["session_id"] = message.session_id

    return result


async def collect_agent_result(
    notebook_path: str,
    user_prompt: str,
    use_subagents: bool = False,
) -> dict:
    """Run agent and collect final result.

    Convenience function that runs the agent to completion
    and returns the final artifact.

    Args:
        notebook_path: Path to the Marimo notebook file
        user_prompt: User's animation request
        use_subagents: Whether to use the dual-agent approach

    Returns:
        dict with patch_type, artifact, and metadata
    """
    generator = (
        generate_with_subagents(notebook_path, user_prompt)
        if use_subagents
        else generate_with_agent(notebook_path, user_prompt)
    )

    result_text = ""
    session_id = None

    async for message in generator:
        if message.get("subtype") == "init":
            session_id = message.get("session_id")
        if "result" in message:
            result_text = message["result"]

    artifact = result_text
    if "```python" in artifact:
        start = artifact.find("```python") + 9
        end = artifact.find("```", start)
        if end > start:
            artifact = artifact[start:end].strip()

    return {
        "patch_type": "cell",
        "artifact": artifact,
        "session_id": session_id,
        "agent_mode": "subagents" if use_subagents else "single",
    }
