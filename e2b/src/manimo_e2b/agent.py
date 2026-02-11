"""Claude Agent SDK execution in E2B sandboxes.

Runs agents in isolated environments with access to workspace files.
"""

from e2b_code_interpreter import Sandbox

from manimo_e2b.config import settings


def run_agent_in_sandbox(
    notebook_id: str,
    user_id: str,
    user_prompt: str,
    use_subagents: bool = False,
    model: str = "claude-sonnet-4-20250514",
    opus_model: str = "claude-opus-4-5-20251101",
) -> dict:
    """
    Run Claude Agent SDK in an isolated E2B sandbox.

    This function executes the agent in a secure, ephemeral environment
    where it can safely use tools like Read, Glob, Grep, and Bash.

    Args:
        notebook_id: ID of the notebook to work with
        user_id: User ID for R2 storage
        user_prompt: User's animation request
        use_subagents: Whether to use dual-agent (planner + coder) approach
        model: Model for code generation (default: Sonnet)
        opus_model: Model for planning (default: Opus)

    Returns:
        dict with patch_type, artifact, session_id, and agent_mode
    """
    r2_bucket = settings.R2_BUCKET
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    # Create sandbox for agent execution
    sandbox = Sandbox(
        template=settings.E2B_TEMPLATE,
        timeout=10 * 60,  # 10 minutes for agent execution
        envs={
            "R2_ENDPOINT": settings.R2_ENDPOINT,
            "R2_ACCESS_KEY_ID": settings.R2_ACCESS_KEY_ID,
            "R2_SECRET_ACCESS_KEY": settings.R2_SECRET_ACCESS_KEY,
            "ANTHROPIC_API_KEY": settings.ANTHROPIC_API_KEY,
        },
    )

    try:
        # Download notebook
        download_script = f'''
import os
import boto3
from pathlib import Path

client = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

workspace = Path("/home/user/workspace")
workspace.mkdir(parents=True, exist_ok=True)

client.download_file("{r2_bucket}", "{notebook_key}", str(workspace / "notebook.py"))
print("Downloaded notebook")
'''
        result = sandbox.commands.run(f"python3 -c '''{download_script}'''")
        if result.error:
            return {"status": "error", "error": f"Download failed: {result.error}"}

        # Build the agent execution script
        # Note: This requires claude-agent-sdk to be installed in the template
        agent_script = _build_agent_script(
            notebook_path="/home/user/workspace/notebook.py",
            user_prompt=user_prompt,
            use_subagents=use_subagents,
            model=model,
            opus_model=opus_model,
        )

        # Run the agent
        result = sandbox.commands.run(f"python3 -c '''{agent_script}'''", timeout=600)

        if result.error:
            return {
                "patch_type": "error",
                "artifact": "",
                "error": result.error,
                "agent_mode": "subagents" if use_subagents else "single",
            }

        # Parse the result - agent script prints JSON at the end
        output = result.stdout or ""

        # Extract the artifact from the output
        artifact = ""
        if "ARTIFACT_START" in output and "ARTIFACT_END" in output:
            start = output.find("ARTIFACT_START") + len("ARTIFACT_START")
            end = output.find("ARTIFACT_END")
            artifact = output[start:end].strip()

        return {
            "patch_type": "cell",
            "artifact": artifact,
            "session_id": sandbox.sandbox_id,
            "agent_mode": "subagents" if use_subagents else "single",
        }

    finally:
        # Clean up sandbox
        try:
            sandbox.kill()
        except Exception:
            pass


def _build_agent_script(
    notebook_path: str,
    user_prompt: str,
    use_subagents: bool,
    model: str,
    opus_model: str,
) -> str:
    """Build the Python script that runs the Claude Agent SDK."""

    system_prompt = '''You are an expert Manim animation developer. Your task is to
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

Output format: Return a complete @app.cell with the Scene class.'''

    # Escape the prompts for embedding in Python string
    escaped_system = system_prompt.replace("'", "\\'").replace('"', '\\"')
    escaped_user = user_prompt.replace("'", "\\'").replace('"', '\\"')

    if use_subagents:
        return f'''
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def run_agent():
    prompt = """Analyze the notebook at {notebook_path} and the user's request.

User request: {escaped_user}

First, use the manim-planner agent to design the animation approach.
Then, use the manim-coder agent to implement the code.

Return the final @app.cell code block."""

    messages = []
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task"],
            cwd="/home/user/workspace",
            agents={{
                "manim-planner": AgentDefinition(
                    description="Plans Manim animation structure and approach",
                    prompt="""You are a Manim animation architect. Analyze the request and:
1. Identify the mathematical concepts to visualize
2. Choose appropriate Manim objects and animations
3. Plan the timing and scene structure
4. List any potential issues or edge cases

Return a structured plan, not code.""",
                    tools=["Read", "Glob", "Grep"],
                    model="{opus_model}",
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
                    model="{model}",
                ),
            }}
        )
    ):
        messages.append(message)

    return messages

messages = asyncio.run(run_agent())

# Extract result
result_text = ""
for message in messages:
    if hasattr(message, "result") and message.result:
        result_text = message.result
    elif hasattr(message, "content") and message.content:
        content = message.content
        if isinstance(content, str):
            result_text = content
        elif isinstance(content, list):
            for block in content:
                if hasattr(block, "text"):
                    result_text = block.text
                elif isinstance(block, dict) and "text" in block:
                    result_text = block["text"]
    elif hasattr(message, "text") and message.text:
        result_text = message.text

# Extract code from markdown if present
artifact = result_text
if "```python" in artifact:
    start = artifact.find("```python") + 9
    end = artifact.find("```", start)
    if end > start:
        artifact = artifact[start:end].strip()
elif "```" in artifact:
    start = artifact.find("```") + 3
    newline = artifact.find("\\n", start)
    if newline > start:
        start = newline + 1
    end = artifact.find("```", start)
    if end > start:
        artifact = artifact[start:end].strip()

print("ARTIFACT_START")
print(artifact)
print("ARTIFACT_END")
'''
    else:
        return f'''
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_agent():
    prompt = """Read the notebook at {notebook_path} and understand its structure.

User request: {escaped_user}

Generate a new @app.cell block with Manim code that fulfills this request.
Follow all Manim best practices for mathematical animations.

Return the complete @app.cell code block."""

    messages = []
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            system_prompt="""{escaped_system}""",
            allowed_tools=["Read", "Glob", "Grep", "Bash"],
            cwd="/home/user/workspace",
            model="{model}",
        )
    ):
        messages.append(message)

    return messages

messages = asyncio.run(run_agent())

# Extract result
result_text = ""
for message in messages:
    if hasattr(message, "result") and message.result:
        result_text = message.result
    elif hasattr(message, "content") and message.content:
        content = message.content
        if isinstance(content, str):
            result_text = content
        elif isinstance(content, list):
            for block in content:
                if hasattr(block, "text"):
                    result_text = block.text
                elif isinstance(block, dict) and "text" in block:
                    result_text = block["text"]
    elif hasattr(message, "text") and message.text:
        result_text = message.text

# Extract code from markdown if present
artifact = result_text
if "```python" in artifact:
    start = artifact.find("```python") + 9
    end = artifact.find("```", start)
    if end > start:
        artifact = artifact[start:end].strip()
elif "```" in artifact:
    start = artifact.find("```") + 3
    newline = artifact.find("\\n", start)
    if newline > start:
        start = newline + 1
    end = artifact.find("```", start)
    if end > start:
        artifact = artifact[start:end].strip()

print("ARTIFACT_START")
print(artifact)
print("ARTIFACT_END")
'''
