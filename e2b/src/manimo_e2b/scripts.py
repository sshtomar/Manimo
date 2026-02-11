"""Embedded scripts for E2B sandbox execution.

These scripts run inside the E2B sandbox to:
- Download notebooks from R2
- Configure Marimo AI integration
- Auto-sync changes back to R2
- Run the AI server for Marimo integration
"""

from manimo_e2b.config import settings


def download_notebook_script(notebook_key: str, r2_bucket: str) -> str:
    """Generate a script that downloads notebook from R2.

    This runs inside the Sandbox with R2 credentials from environment.
    """
    base_path = "/".join(notebook_key.split("/")[:-1])

    return f'''
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

workspace_path = "/home/user/workspace"
base_path = "{base_path}"

# Ensure workspace exists
Path(workspace_path).mkdir(parents=True, exist_ok=True)

# Download notebook.py
notebook_path = f"{{workspace_path}}/notebook.py"
try:
    client.download_file("{r2_bucket}", "{notebook_key}", notebook_path)
    print(f"Downloaded notebook: {notebook_key}")
except Exception as e:
    print(f"Download error: {{e}}")
    # Create default notebook if download fails
    lines = [
        "import marimo",
        "app = marimo.App()",
        "",
        "@app.cell",
        "def __():",
        "    import marimo as mo",
        "    return (mo,)",
        "",
        "if __name__ == '__main__':",
        "    app.run()",
    ]
    Path(notebook_path).write_text(chr(10).join(lines))
    print("Created default notebook")

# Download data files if they exist
data_prefix = f"{{base_path}}/data/"
try:
    response = client.list_objects_v2(Bucket="{r2_bucket}", Prefix=data_prefix)
    if "Contents" in response:
        data_dir = Path(workspace_path) / "data"
        data_dir.mkdir(exist_ok=True)
        for obj in response["Contents"]:
            key = obj["Key"]
            filename = key.replace(data_prefix, "")
            if filename:
                local_path = data_dir / filename
                local_path.parent.mkdir(parents=True, exist_ok=True)
                client.download_file("{r2_bucket}", key, str(local_path))
                print(f"Downloaded data file: {{filename}}")
except Exception as e:
    print(f"Data download info: {{e}}")

print("\\nWorkspace ready at /home/user/workspace")
'''


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


def marimo_config_script() -> str:
    """Generate script that writes Marimo configuration file."""
    import base64
    config_content = generate_marimo_config("http://127.0.0.1:8081/v1")
    config_b64 = base64.b64encode(config_content.encode()).decode()
    return f'''
import base64
from pathlib import Path

config_b64 = "{config_b64}"
config_content = base64.b64decode(config_b64).decode()

config_path = Path("/home/user/.config/marimo/marimo.toml")
config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(config_content)
print(f"Wrote Marimo config to {{config_path}}")
'''


def auto_sync_script(r2_bucket: str, base_path: str) -> str:
    """Generate background auto-sync process for saving notebook changes to R2.

    Watches /home/user/workspace/ for changes and uploads to R2 every 5 seconds.
    Uses SHA256 to detect actual content changes.
    """
    return f'''
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
    """Sync all tracked files in workspace."""
    workspace = Path("/home/user/workspace")

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


# Agent server script - OpenAI-compatible API for Marimo AI integration
AGENT_SERVER_SCRIPT = '''
"""OpenAI-compatible API server for Marimo AI integration.

This runs inside the sandbox on port 8081, providing AI assistance with
full file system access to /home/user/workspace/.
"""
import os
import json
import asyncio
from pathlib import Path
from typing import Any
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

# Initialize Anthropic clients
try:
    sync_client = anthropic.Anthropic()
    async_client = anthropic.AsyncAnthropic()
    logger.info("Anthropic clients initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Anthropic clients: {e}")

# System prompt for statistical/data analysis focus
SYSTEM_PROMPT = """You are an expert data analyst and statistician working in a Marimo notebook.
You have access to the workspace at /home/user/workspace/ containing the notebook and any data files.

When helping users:
1. Always examine actual data before generating code
2. Use proper statistical methods with reproducibility
3. Generate clean, well-commented Marimo cell code
4. Follow Marimo patterns: reactive cells, proper variable returns
5. For visualizations, prefer matplotlib/seaborn with proper labeling

You can read files in /home/user/workspace/ to understand the data and notebook structure."""


def normalize_content(content: Any) -> str:
    """Normalize message content to a string."""
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
    content: Any

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
        full_path = Path("/home/user/workspace") / path.lstrip("/")
        if full_path.exists() and full_path.is_file():
            return full_path.read_text()[:50000]
    except OSError:
        pass
    return None


def list_workspace_files() -> list[str]:
    """List all files in the workspace."""
    files = []
    workspace = Path("/home/user/workspace")
    if workspace.exists():
        for f in workspace.rglob("*"):
            if f.is_file():
                files.append(str(f.relative_to(workspace)))
    return files[:100]


def build_context() -> str:
    """Build context about the workspace for the AI."""
    files = list_workspace_files()
    context_parts = ["\\n## Workspace Files\\n"]
    for f in files:
        context_parts.append(f"- {f}")

    notebook_content = read_workspace_file("notebook.py")
    if notebook_content:
        context_parts.append("\\n## Current Notebook\\n```python")
        context_parts.append(notebook_content[:10000])
        context_parts.append("```")

    return "\\n".join(context_parts)


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint."""
    import time
    logger.info(f"Chat request: model={request.model}, stream={request.stream}")

    context = build_context()
    messages = []
    extra_system = []

    for msg in request.messages:
        if msg.role == "system":
            extra_system.append(msg.content)
            continue

        if msg.role == "user" and len(messages) == 0:
            messages.append({
                "role": "user",
                "content": f"{context}\\n\\n---\\n\\n{msg.content}"
            })
        else:
            messages.append({"role": msg.role, "content": msg.content})

    system_prompt = SYSTEM_PROMPT
    if extra_system:
        system_prompt = SYSTEM_PROMPT + "\\n\\n" + "\\n".join(extra_system)

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
    """Stream the response in SSE format."""
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
        yield f"data: {json.dumps(build_chunk({'role': 'assistant'}))}\\n\\n"

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
                    yield f"data: {json.dumps(build_chunk({}, 'stop'))}\\n\\n"
                    break

        yield "data: [DONE]\\n\\n"
        logger.info("Streaming complete")

    except Exception as e:
        logger.error(f"Streaming error: {e}")
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
