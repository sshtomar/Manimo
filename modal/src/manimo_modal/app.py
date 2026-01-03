"""Main Modal app definition for Manimo notebooks."""

import modal
from pathlib import Path

# Image with Manim and Marimo (for basic sessions)
notebook_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "ffmpeg",
        "texlive",
        "texlive-latex-extra",
        "texlive-fonts-extra",
        "texlive-latex-recommended",
        # Cairo and Pango dependencies for manimpango
        "libcairo2-dev",
        "libpango1.0-dev",
        "pkg-config",
        "python3-dev",
        "build-essential",
    )
    .pip_install("uv")
    .run_commands(
        "uv pip install --system marimo>=0.17.8 boto3>=1.34.0 manim>=0.18.0"
    )
)

# Full sandbox image with AI capabilities
sandbox_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "ffmpeg",
        "texlive",
        "texlive-latex-extra",
        "texlive-fonts-extra",
        "texlive-latex-recommended",
        "libcairo2-dev",
        "libpango1.0-dev",
        "pkg-config",
        "python3-dev",
        "build-essential",
    )
    .pip_install("uv")
    .run_commands(
        "uv pip install --system "
        "marimo>=0.17.8 "
        "boto3>=1.34.0 "
        "manim>=0.18.0 "
        "anthropic>=0.25.0 "
        "openai>=1.12.0 "
        "fastapi>=0.109.0 "
        "uvicorn>=0.27.0 "
        "httpx>=0.26.0 "
        "pydantic>=2.5.0 "
        "pandas>=2.1.0 "
        "numpy>=1.26.0 "
        "polars>=0.20.0 "
        "scipy>=1.12.0 "
        "statsmodels>=0.14.0 "
        "matplotlib>=3.8.0 "
        "seaborn>=0.13.0 "
        "plotly>=5.18.0 "
        "altair>=5.2.0 "
        "openpyxl>=3.1.0 "
        "xlsxwriter>=3.1.0 "
        "scikit-learn>=1.4.0 "
        "requests>=2.31.0 "
    )
    .run_commands("mkdir -p /root/.config/marimo")
)

app = modal.App("manimo-notebooks")


def download_notebook_script(notebook_key: str, r2_bucket: str) -> str:
    """
    Generate a shell script that downloads notebook from R2.
    This runs inside the Sandbox with R2 credentials.
    """
    base_path = "/".join(notebook_key.split("/")[:-1])

    return f"""
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

workspace_path = "/workspace"
base_path = "{base_path}"

# Download notebook.py
notebook_path = "/workspace/notebook.py"
try:
    client.download_file("{r2_bucket}", "{notebook_key}", notebook_path)
    print(f"✓ Downloaded notebook: {notebook_key}")
except Exception as e:
    print(f"Download error: {{e}}")
    Path(notebook_path).write_text('''
import marimo
app = marimo.App()

@app.cell
def __():
    import marimo as mo
    return mo.md(\\'\\'\\'# Error

    Could not load {notebook_key}

    {{str(e)}}
    \\'\\'\\'),
''')

print("\\nWorkspace ready at /workspace")
"""


def create_proxy_script(notebook_id: str, user_id: str = "default") -> str:
    """
    Create a proxy script that downloads notebook and starts Marimo server.
    """
    r2_bucket = "manimo-notebooks"
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    download_script = download_notebook_script(notebook_key, r2_bucket)

    return f"""
import subprocess
import sys

# Download notebook
exec({repr(download_script)})

# Start Marimo server
subprocess.run([
    sys.executable, "-m", "marimo", "edit",
    "--port", "8080",
    "--host", "0.0.0.0",
    "/workspace/notebook.py"
])
"""


@app.function(
    image=notebook_image,
    secrets=[modal.Secret.from_name("r2-credentials")],
    timeout=3600,  # 1 hour timeout
)
def launch_marimo_session(notebook_id: str, user_id: str = "default") -> dict:
    """
    Launch a Marimo edit session for a notebook.

    Creates a sandbox, downloads notebook from R2, and starts Marimo server.
    Returns the tunnel URL for accessing the Marimo UI.
    """
    r2_bucket = "manimo-notebooks"
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    # Create a script that downloads notebook and starts Marimo
    download_script = download_notebook_script(notebook_key, r2_bucket)
    
    startup_script = f"""
import os
import subprocess
import sys
from pathlib import Path

# Ensure workspace exists
workspace_path = Path("/workspace")
workspace_path.mkdir(parents=True, exist_ok=True)

# Download notebook
{download_script}

# Start Marimo server (don't wait - let it run in background)
print("Starting Marimo server...")
notebook_path = "/workspace/notebook.py"
proc = subprocess.Popen([
    sys.executable, "-m", "marimo", "edit",
    "--port", "8080",
    "--host", "0.0.0.0",
    notebook_path
])
# Keep script alive by waiting for the process
proc.wait()
"""

    # Create sandbox with the startup script
    # The sandbox will run this script which starts Marimo
    sandbox = modal.Sandbox.create(
        "python", "-c", startup_script,
        encrypted_ports=[8080],
        secrets=[modal.Secret.from_name("r2-credentials")],
        timeout=30 * 60,  # 30 minutes
        image=notebook_image,
    )

    # Get tunnel URL
    tunnel = sandbox.tunnels()[8080]
    url = tunnel.url
    
    print(f"\n✅ Notebook session launched!")
    print(f"📓 Notebook ID: {notebook_id}")
    print(f"🌐 Tunnel URL: {url}")
    print(f"📊 Status: running")
    print(f"\n🔗 Open this URL in your browser to access the notebook:")
    print(f"   {url}")

    return {
        "notebook_id": notebook_id,
        "url": url,
        "status": "running",
    }


@app.function(
    image=notebook_image,
    secrets=[modal.Secret.from_name("r2-credentials")],
    gpu="T4",  # GPU for video rendering
    timeout=3600,
)
def render_manim_video(
    notebook_id: str,
    user_id: str,
    scene_name: str | None = None,
    quality: str = "medium",
) -> dict:
    """
    Render a Manim video from a notebook.

    Args:
        notebook_id: Notebook ID
        user_id: User ID
        scene_name: Specific scene to render, or None for all scenes
        quality: "low" | "medium" | "high" | "production"

    Returns:
        dict with video_key, status, video_url
    """
    import boto3
    import os
    import subprocess
    import sys
    from pathlib import Path

    r2_bucket = "manimo-notebooks"
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    # Download notebook
    client = boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )

    workspace_path = Path("/workspace")
    notebook_path = workspace_path / "notebook.py"
    client.download_file(r2_bucket, notebook_key, str(notebook_path))

    # Import notebook module to get Scene classes
    import importlib.util
    spec = importlib.util.spec_from_file_location("notebook", str(notebook_path))
    notebook_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notebook_module)

    # Find Scene classes
    scene_classes = [
        name for name, obj in notebook_module.__dict__.items()
        if isinstance(obj, type) and issubclass(obj, type) and hasattr(obj, "construct")
    ]

    if not scene_classes:
        return {
            "status": "error",
            "error": "No Scene classes found in notebook",
        }

    # Render scenes
    videos_dir = workspace_path / "videos"
    videos_dir.mkdir(exist_ok=True)

    rendered_videos = []
    for scene_class_name in scene_classes:
        if scene_name and scene_class_name != scene_name:
            continue

        # Map quality to Manim quality flags
        quality_map = {
            "low": "low_quality",
            "medium": "medium_quality",
            "high": "high_quality",
            "production": "production_quality",
        }
        quality_flag = quality_map.get(quality, "medium_quality")

        # Render scene
        output_file = videos_dir / f"{scene_class_name}.mp4"
        result = subprocess.run(
            [
                sys.executable, "-m", "manim",
                str(notebook_path),
                scene_class_name,
                f"--{quality_flag}",
                "-o", str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0 and output_file.exists():
            # Upload to R2
            video_key = f"{user_id}/{notebook_id}/videos/{scene_class_name}.mp4"
            client.upload_file(
                str(output_file),
                r2_bucket,
                video_key,
                ExtraArgs={"ContentType": "video/mp4"},
            )
            rendered_videos.append(video_key)

    return {
        "status": "completed",
        "videos": rendered_videos,
    }


# Image for Claude Agent SDK execution
agent_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("nodejs", "npm", "git")
    .run_commands("npm install -g @anthropic-ai/claude-code")
    .pip_install(
        "claude-agent-sdk>=0.1.0",
        "boto3>=1.34.0",
        "anthropic>=0.25.0",
    )
)


@app.function(
    image=agent_image,
    secrets=[
        modal.Secret.from_name("r2-credentials"),
        modal.Secret.from_name("anthropic-api-key"),
    ],
    timeout=600,  # 10 minute timeout for agent execution
    cpu=1.0,
    memory=1024,
)
def run_agent_in_sandbox(
    notebook_id: str,
    user_id: str,
    user_prompt: str,
    use_subagents: bool = False,
    model: str = "claude-sonnet-4-20250514",
    opus_model: str = "claude-opus-4-5-20251101",
) -> dict:
    """
    Run Claude Agent SDK in an isolated Modal sandbox.

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
    import asyncio
    import os
    import boto3
    from pathlib import Path

    from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

    # Download notebook from R2
    r2_bucket = os.environ.get("R2_BUCKET", "manimo-notebooks")
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    client = boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )

    workspace = Path("/workspace")
    workspace.mkdir(parents=True, exist_ok=True)
    notebook_path = workspace / "notebook.py"

    client.download_file(r2_bucket, notebook_key, str(notebook_path))
    print(f"✓ Downloaded notebook: {notebook_key}")

    # System prompt for Manim generation
    system_prompt = """You are an expert Manim animation developer. Your task is to
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

    async def run_agent():
        if use_subagents:
            # Dual-agent mode: Planner (Opus) + Coder (Sonnet)
            prompt = f"""Analyze the notebook at {notebook_path} and the user's request.

User request: {user_prompt}

First, use the manim-planner agent to design the animation approach.
Then, use the manim-coder agent to implement the code.

Return the final @app.cell code block."""

            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    allowed_tools=["Read", "Glob", "Grep", "Task"],
                    cwd=str(workspace),
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
                            model=opus_model,
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
                            model=model,
                        ),
                    }
                )
            ):
                messages.append(message)
        else:
            # Single agent mode
            prompt = f"""Read the notebook at {notebook_path} and understand its structure.

User request: {user_prompt}

Generate a new @app.cell block with Manim code that fulfills this request.
Follow all Manim best practices for mathematical animations.

Return the complete @app.cell code block."""

            messages = []
            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    allowed_tools=["Read", "Glob", "Grep", "Bash"],
                    cwd=str(workspace),
                    model=model,
                )
            ):
                messages.append(message)

        return messages

    # Run the async agent
    messages = asyncio.run(run_agent())

    # Extract result - check multiple possible attributes
    result_text = ""
    session_id = None

    for message in messages:
        if hasattr(message, "subtype") and message.subtype == "init":
            session_id = getattr(message, "session_id", None)

        # Check for result in various attributes
        if hasattr(message, "result") and message.result:
            result_text = message.result
        elif hasattr(message, "content") and message.content:
            # Content might be a string or a list of content blocks
            content = message.content
            if isinstance(content, str):
                result_text = content
            elif isinstance(content, list):
                # Extract text from content blocks
                for block in content:
                    if hasattr(block, "text"):
                        result_text = block.text
                    elif isinstance(block, dict) and "text" in block:
                        result_text = block["text"]
        elif hasattr(message, "text") and message.text:
            result_text = message.text

    # Debug: print message types for troubleshooting
    print(f"Processed {len(messages)} messages, result length: {len(result_text)}")

    # Extract code from markdown if present
    artifact = result_text
    if "```python" in artifact:
        start = artifact.find("```python") + 9
        end = artifact.find("```", start)
        if end > start:
            artifact = artifact[start:end].strip()
    elif "```" in artifact:
        # Try generic code block
        start = artifact.find("```") + 3
        # Skip language identifier if present
        newline = artifact.find("\n", start)
        if newline > start:
            start = newline + 1
        end = artifact.find("```", start)
        if end > start:
            artifact = artifact[start:end].strip()

    return {
        "patch_type": "cell",
        "artifact": artifact,
        "session_id": session_id,
        "agent_mode": "subagents" if use_subagents else "single",
    }


# =============================================================================
# In-Sandbox Agent SDK Server (OpenAI-compatible API on port 8081)
# =============================================================================

AGENT_SERVER_SCRIPT = '''
"""OpenAI-compatible API server for Marimo AI integration.

This runs inside the sandbox on port 8081, providing AI assistance with
full file system access to /workspace/.
"""
import os
import json
import hashlib
import asyncio
from pathlib import Path
from typing import Any, Union
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator
import uvicorn

app = FastAPI(title="Manimo AI Server")

# Setup logging to file for debugging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/ai-server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Anthropic clients (sync for non-streaming, async for streaming)
try:
    sync_client = anthropic.Anthropic()
    async_client = anthropic.AsyncAnthropic()
    logger.info("Anthropic clients initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Anthropic clients: {e}")

# System prompt for statistical/data analysis focus
SYSTEM_PROMPT = """You are an expert data analyst and statistician working in a Marimo notebook.
You have access to the workspace at /workspace/ containing the notebook and any data files.

When helping users:
1. Always examine actual data before generating code
2. Use proper statistical methods with reproducibility
3. Generate clean, well-commented Marimo cell code
4. Follow Marimo patterns: reactive cells, proper variable returns
5. For visualizations, prefer matplotlib/seaborn with proper labeling

You can read files in /workspace/ to understand the data and notebook structure."""


def normalize_content(content: Any) -> str:
    """Normalize message content to a string.

    Handles both plain strings and OpenAI vision-format content blocks:
    - "hello" -> "hello"
    - [{"type": "text", "text": "hello"}] -> "hello"
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)
        return "\\n".join(text_parts)
    return str(content)


class ChatMessage(BaseModel):
    role: str
    content: Any  # Accept any type, normalize in validator

    @field_validator("content", mode="before")
    @classmethod
    def normalize_content_field(cls, v: Any) -> str:
        return normalize_content(v)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool = False
    temperature: float = 0.7
    max_tokens: int = 4096


def read_workspace_file(path: str) -> str | None:
    """Read a file from the workspace."""
    try:
        full_path = Path("/workspace") / path.lstrip("/")
        if full_path.exists() and full_path.is_file():
            return full_path.read_text()[:50000]  # Limit to 50KB
    except OSError:
        pass
    return None


def list_workspace_files() -> list[str]:
    """List all files in the workspace."""
    files = []
    workspace = Path("/workspace")
    if workspace.exists():
        for f in workspace.rglob("*"):
            if f.is_file():
                files.append(str(f.relative_to(workspace)))
    return files[:100]  # Limit to 100 files


def build_context() -> str:
    """Build context about the workspace for the AI."""
    files = list_workspace_files()
    context_parts = ["\\n## Workspace Files\\n"]
    for f in files:
        context_parts.append(f"- {f}")

    # Read notebook if exists
    notebook_content = read_workspace_file("notebook.py")
    if notebook_content:
        context_parts.append("\\n## Current Notebook\\n```python")
        context_parts.append(notebook_content[:10000])
        context_parts.append("```")

    return "\\n".join(context_parts)


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint.

    NOTE: We always return non-streaming responses regardless of request.stream.
    This matches Inquiro's working implementation and avoids Marimo streaming issues.
    """
    import time
    logger.info(f"Chat request: model={request.model}, stream={request.stream}, messages={len(request.messages)}")

    # Build messages with context
    context = build_context()
    messages = []
    extra_system = []

    for msg in request.messages:
        # Anthropic doesn't accept "system" role in messages - extract to system prompt
        if msg.role == "system":
            extra_system.append(msg.content)
            continue

        if msg.role == "user" and len(messages) == 0:
            # Add context to first user message
            messages.append({
                "role": "user",
                "content": f"{context}\\n\\n---\\n\\n{msg.content}"
            })
        else:
            messages.append({"role": msg.role, "content": msg.content})

    # Combine system prompts
    system_prompt = SYSTEM_PROMPT
    if extra_system:
        system_prompt = SYSTEM_PROMPT + "\\n\\n" + "\\n".join(extra_system)

    # Map model names
    model_map = {
        "manimo/statistical-v1": "claude-haiku-4-5-20251001",
        "manimo/statistical-v1-fast": "claude-haiku-4-5-20251001",
        "gpt-4": "claude-sonnet-4-20250514",
        "gpt-3.5-turbo": "claude-haiku-4-5-20251001",
    }
    model = model_map.get(request.model, "claude-haiku-4-5-20251001")
    logger.info(f"Using model: {model}")

    try:
        if request.stream:
            logger.info("Starting streaming response")
            return StreamingResponse(
                stream_response(model, messages, request.max_tokens, request.temperature, request.model, system_prompt),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )
        else:
            logger.info("Starting non-streaming response")
            response = sync_client.messages.create(
                model=model,
                max_tokens=request.max_tokens,
                system=system_prompt,
                messages=messages,
            )

            response_text = response.content[0].text if response.content else ""
            logger.info(f"Response received: {len(response_text)} chars")

            return {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }
    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def stream_response(model: str, messages: list, max_tokens: int, temperature: float, original_model: str, system_prompt: str):
    """Stream the response in SSE format matching OpenAI/Inquiro format exactly."""
    import time
    import uuid
    logger.info(f"stream_response started: model={model}")

    created = int(time.time())
    response_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"

    def build_chunk(delta: dict = None, finish_reason: str = None) -> dict:
        return {
            "id": response_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": original_model,
            "choices": [{
                "index": 0,
                "delta": delta or {},
                "finish_reason": finish_reason
            }]
        }

    try:
        # Initial chunk with role only (no content) - matches Inquiro format
        yield f"data: {json.dumps(build_chunk({'role': 'assistant'}))}\\n\\n"

        # Use raw event stream for more control
        async with async_client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    delta = event.delta
                    if hasattr(delta, "text") and delta.text:
                        yield f"data: {json.dumps(build_chunk({'content': delta.text}))}\\n\\n"

                elif event.type == "message_stop":
                    # Final chunk with finish_reason
                    yield f"data: {json.dumps(build_chunk({}, 'stop'))}\\n\\n"
                    break

        yield "data: [DONE]\\n\\n"
        logger.info("Streaming complete")

    except Exception as e:
        logger.error(f"Streaming error: {e}")
        import traceback
        traceback.print_exc()
        # Send error as content so user sees it
        yield f"data: {json.dumps(build_chunk({'content': f'Error: {e}'}))}\\n\\n"
        yield f"data: {json.dumps(build_chunk({}, 'stop'))}\\n\\n"
        yield "data: [DONE]\\n\\n"


@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            {"id": "manimo/statistical-v1", "object": "model", "owned_by": "manimo"},
            {"id": "manimo/statistical-v1-fast", "object": "model", "owned_by": "manimo"},
        ]
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
'''


# =============================================================================
# Marimo Configuration Generator
# =============================================================================

def generate_marimo_config(api_base_url: str = "http://127.0.0.1:8081") -> str:
    """Generate marimo.toml configuration for AI integration."""
    return f'''# Marimo configuration for Manimo notebooks
# Auto-generated - do not edit manually

[runtime]
on_cell_change = "lazy"
auto_instantiate = false
auto_reload = "off"
output_max_bytes = 8000000
std_stream_max_bytes = 1000000

[ai]
mode = "ask"
inline_tooltip = false
rules = """You are Manimo's Manim animation assistant. You help create mathematical
visualizations using Manim in Marimo notebooks. Always follow Manim best practices:
use proper Scene class structure, include clear comments, use appropriate timing.
IMPORTANT: When analyzing the notebook, use the available tools to inspect the
current code structure before generating new cells."""

[ai.open_ai_compatible]
api_key = "manimo-internal"
base_url = "{api_base_url}"

[ai.models]
chat_model = "manimo/statistical-v1"
edit_model = "manimo/statistical-v1"
autocomplete_model = "manimo/statistical-v1"
custom_models = ["manimo/statistical-v1"]
displayed_models = []

[completion]
activate_on_typing = true
copilot = "custom"

[package_management]
manager = "uv"

[display]
theme = "light"
code_editor_font_size = 14
cell_output = "below"
default_width = "medium"
dataframes = "rich"

[save]
autosave = "after_delay"
autosave_delay = 1000
format_on_save = false

[formatting]
line_length = 88

[keymap]
preset = "default"
'''


MARIMO_CONFIG_SCRIPT = '''
"""Write Marimo configuration file."""
from pathlib import Path

config_content = {config_content!r}

config_path = Path("/root/.config/marimo/marimo.toml")
config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(config_content)
print(f"Wrote Marimo config to {{config_path}}")
'''


# =============================================================================
# Auto-Sync to R2 Background Process
# =============================================================================

AUTO_SYNC_SCRIPT = '''
"""Background auto-sync process for saving notebook changes to R2.

Watches /workspace/ for changes and uploads to R2 every 5 seconds.
Uses SHA256 to detect actual content changes.
"""
import os
import time
import hashlib
from pathlib import Path
import boto3

# R2 configuration
R2_BUCKET = "{r2_bucket}"
BASE_PATH = "{base_path}"
SYNC_INTERVAL = 5  # seconds

# Initialize R2 client
client = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

# Track file hashes to detect changes
file_hashes = {{}}

def compute_hash(path: Path) -> str:
    """Compute SHA256 hash of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sync_file(local_path: Path, remote_key: str):
    """Upload a file to R2 if changed."""
    if not local_path.exists():
        return

    current_hash = compute_hash(local_path)
    if file_hashes.get(str(local_path)) == current_hash:
        return  # No change

    try:
        client.upload_file(
            str(local_path),
            R2_BUCKET,
            remote_key,
        )
        file_hashes[str(local_path)] = current_hash
        print(f"Synced: {{remote_key}}")
    except Exception as e:
        print(f"Sync error for {{remote_key}}: {{e}}")

def sync_workspace():
    """Sync all tracked files in /workspace/."""
    workspace = Path("/workspace")

    # Sync notebook
    notebook_path = workspace / "notebook.py"
    if notebook_path.exists():
        sync_file(notebook_path, f"{{BASE_PATH}}/notebook.py")

    # Sync data files
    data_dir = workspace / "data"
    if data_dir.exists():
        for f in data_dir.rglob("*"):
            if f.is_file():
                relative = f.relative_to(workspace)
                sync_file(f, f"{{BASE_PATH}}/{{relative}}")

    # Sync images
    images_dir = workspace / "images"
    if images_dir.exists():
        for f in images_dir.rglob("*"):
            if f.is_file():
                relative = f.relative_to(workspace)
                sync_file(f, f"{{BASE_PATH}}/{{relative}}")

print("Starting auto-sync to R2...")
print(f"Bucket: {{R2_BUCKET}}")
print(f"Path: {{BASE_PATH}}")
print(f"Interval: {{SYNC_INTERVAL}}s")

while True:
    try:
        sync_workspace()
    except Exception as e:
        print(f"Sync cycle error: {{e}}")
    time.sleep(SYNC_INTERVAL)
'''


# =============================================================================
# Full Notebook Sandbox with AI Integration
# =============================================================================

@app.function(
    image=sandbox_image,
    secrets=[
        modal.Secret.from_name("r2-credentials"),
        modal.Secret.from_name("anthropic-api-key"),
    ],
    timeout=180,
    min_containers=1,  # Keep warm for fast startup
)
def spawn_notebook_sandbox(
    notebook_id: str,
    user_id: str = "default",
) -> dict:
    """
    Spawn a full Marimo notebook sandbox with AI integration.

    Timeline:
    [T+0.0s] Create sandbox with sleep infinity (keeps container alive)
    [T+5.2s] Download notebook + data from R2 to /workspace/
    [T+5.4s] Create marimo.toml with AI configuration
    [T+5.6s] Start auto-sync background process
    [T+6.0s] Start Agent SDK server on port 8081
    [T+6.5s] Start Marimo on port 8080
    [T+7.0s] Return tunnel URL immediately

    Args:
        notebook_id: ID of the notebook to open
        user_id: User ID for R2 storage path

    Returns:
        dict with marimo_url, status, sandbox_id
    """
    r2_bucket = "manimo-notebooks"
    base_path = f"{user_id}/{notebook_id}"
    notebook_key = f"{base_path}/notebook.py"

    # Generate all the scripts
    download_script = download_notebook_script(notebook_key, r2_bucket)

    config_content = generate_marimo_config("http://127.0.0.1:8081/v1")
    config_script = MARIMO_CONFIG_SCRIPT.format(config_content=config_content)

    sync_script = AUTO_SYNC_SCRIPT.format(
        r2_bucket=r2_bucket,
        base_path=base_path,
    )

    # Create sandbox that stays alive
    sandbox = modal.Sandbox.create(
        "sleep", "infinity",
        encrypted_ports=[8080],  # Only expose Marimo UI
        secrets=[
            modal.Secret.from_name("r2-credentials"),
            modal.Secret.from_name("anthropic-api-key"),
        ],
        timeout=30 * 60,  # 30 minutes
        cpu=2.0,
        memory=4096,
        image=sandbox_image,
    )

    print(f"Sandbox created: {sandbox.object_id}")

    # Step 1: Create workspace and download notebook
    print("Downloading notebook from R2...")
    sandbox.exec("mkdir", "-p", "/workspace")
    proc = sandbox.exec("python", "-c", download_script)
    proc.wait()

    # Step 2: Write Marimo configuration
    print("Writing Marimo configuration...")
    proc = sandbox.exec("python", "-c", config_script)
    proc.wait()

    # Step 3: Start auto-sync in background
    print("Starting auto-sync...")
    sandbox.exec("python", "-c", sync_script)  # No .wait() - runs in background

    # Step 4: Start Agent SDK server on port 8081
    print("Starting AI server on port 8081...")
    sandbox.exec("python", "-c", AGENT_SERVER_SCRIPT)  # No .wait() - runs in background

    # Give servers a moment to start
    import time
    time.sleep(1)

    # Step 5: Start Marimo with AI configuration
    print("Starting Marimo on port 8080...")
    sandbox.exec(
        "sh", "-c",
        "cd /workspace && "
        "OPENAI_API_KEY=manimo-internal "
        "OPENAI_BASE_URL=http://127.0.0.1:8081/v1 "
        "python -m marimo edit notebook.py "
        "--host 0.0.0.0 --port 8080 --headless --no-token"
    )  # No .wait() - runs in background

    # Get tunnel URL and return immediately
    tunnel = sandbox.tunnels()[8080]

    print(f"\\nNotebook sandbox ready!")
    print(f"Notebook ID: {notebook_id}")
    print(f"Marimo URL: {tunnel.url}")
    print(f"Sandbox ID: {sandbox.object_id}")

    return {
        "marimo_url": tunnel.url,
        "status": "launching",
        "sandbox_id": sandbox.object_id,
        "notebook_id": notebook_id,
    }


@app.function(
    image=sandbox_image,
    timeout=60,
)
def check_sandbox_status(sandbox_id: str) -> dict:
    """Check the status of a running sandbox."""
    try:
        sandbox = modal.Sandbox.from_id(sandbox_id)
        # Try to check if it's still running
        return {
            "status": "running",
            "active": True,
            "sandbox_id": sandbox_id,
        }
    except modal.exception.NotFoundError:
        return {
            "status": "terminated",
            "active": False,
            "sandbox_id": sandbox_id,
        }
    except Exception as e:
        return {
            "status": "error",
            "active": False,
            "sandbox_id": sandbox_id,
            "error": str(e),
        }

