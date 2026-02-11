"""E2B sandbox management for Marimo notebooks.

Provides functions to spawn and manage E2B sandboxes for notebook editing.
"""

import time
from e2b_code_interpreter import Sandbox

from manimo_e2b.config import settings
from manimo_e2b.scripts import (
    download_notebook_script,
    marimo_config_script,
    auto_sync_script,
    AGENT_SERVER_SCRIPT,
)


def spawn_notebook_sandbox(
    notebook_id: str,
    user_id: str = "default",
) -> dict:
    """
    Spawn a full Marimo notebook sandbox with AI integration.

    Timeline:
    [T+0.0s] Create E2B sandbox
    [T+2.8s] Download notebook + data from R2 to /home/user/workspace/
    [T+3.0s] Create marimo.toml with AI configuration
    [T+3.2s] Start auto-sync background process
    [T+3.5s] Start Agent SDK server on port 8081
    [T+4.0s] Start Marimo on port 8080
    [T+4.5s] Return URL immediately

    Args:
        notebook_id: ID of the notebook to open
        user_id: User ID for R2 storage path

    Returns:
        dict with marimo_url, status, sandbox_id, notebook_id
    """
    start_time = time.time()
    r2_bucket = settings.R2_BUCKET
    base_path = f"{user_id}/{notebook_id}"
    notebook_key = f"{base_path}/notebook.py"

    # Generate scripts
    download_script = download_notebook_script(notebook_key, r2_bucket)
    config_script = marimo_config_script()
    sync_script = auto_sync_script(r2_bucket, base_path)

    print(f"[T+0.0s] Creating E2B sandbox...")

    # Create sandbox with environment variables
    # Use None for template if empty string (uses default code-interpreter)
    template = settings.E2B_TEMPLATE if settings.E2B_TEMPLATE else None
    sandbox = Sandbox.create(
        template=template,
        timeout=settings.E2B_TIMEOUT,
        api_key=settings.E2B_API_KEY,
        envs={
            "R2_ENDPOINT": settings.R2_ENDPOINT,
            "R2_ACCESS_KEY_ID": settings.R2_ACCESS_KEY_ID,
            "R2_SECRET_ACCESS_KEY": settings.R2_SECRET_ACCESS_KEY,
            "ANTHROPIC_API_KEY": settings.ANTHROPIC_API_KEY,
        },
    )

    sandbox_time = time.time() - start_time
    print(f"[T+{sandbox_time:.1f}s] Sandbox created: {sandbox.sandbox_id}")

    # Install required packages
    print("Installing required packages...")
    sandbox.commands.run("pip install -q boto3 marimo anthropic openai fastapi uvicorn httpx")

    # Step 1: Create workspace and download notebook
    print("Downloading notebook from R2...")
    sandbox.commands.run("mkdir -p /home/user/workspace")
    result = sandbox.commands.run(f"python3 -c '''{download_script}'''")
    if result.error:
        print(f"Download warning: {result.error}")

    # Step 2: Write Marimo configuration
    print("Writing Marimo configuration...")
    result = sandbox.commands.run(f"python3 -c '''{config_script}'''")
    if result.error:
        print(f"Config warning: {result.error}")

    # Step 3: Start auto-sync in background (skip for now - causes issues)
    # print("Starting auto-sync...")
    # sandbox.commands.run(f"python3 -c '''{sync_script}'''", background=True)

    # Step 4: Start Agent SDK server on port 8081
    # Write script to file first to avoid escaping issues
    print("Starting AI server on port 8081...")
    sandbox.files.write("/tmp/ai_server.py", AGENT_SERVER_SCRIPT)
    sandbox.commands.run("python3 /tmp/ai_server.py", background=True)

    # Give servers a moment to start
    time.sleep(1)

    # Step 5: Start Marimo with AI configuration
    print("Starting Marimo on port 8080...")
    sandbox.commands.run(
        "cd /home/user/workspace && "
        "OPENAI_API_KEY=manimo-internal "
        "OPENAI_BASE_URL=http://127.0.0.1:8081/v1 "
        "python3 -m marimo edit notebook.py "
        "--host 0.0.0.0 --port 8080 --headless --no-token",
        background=True,
    )

    # Get URL
    marimo_host = sandbox.get_host(8080)
    marimo_url = f"https://{marimo_host}"

    total_time = time.time() - start_time
    print(f"\n[T+{total_time:.1f}s] Notebook sandbox ready!")
    print(f"Notebook ID: {notebook_id}")
    print(f"Marimo URL: {marimo_url}")
    print(f"Sandbox ID: {sandbox.sandbox_id}")

    return {
        "marimo_url": marimo_url,
        "status": "launching",
        "sandbox_id": sandbox.sandbox_id,
        "notebook_id": notebook_id,
    }


def check_sandbox_status(sandbox_id: str) -> dict:
    """Check the status of a running sandbox.

    Args:
        sandbox_id: The E2B sandbox ID

    Returns:
        dict with status, active, sandbox_id, and optionally error
    """
    try:
        sandbox = Sandbox.reconnect(sandbox_id)
        # Try a simple command to verify it's responsive
        result = sandbox.commands.run("echo ok", timeout=5)
        if result.error:
            return {
                "status": "error",
                "active": False,
                "sandbox_id": sandbox_id,
                "error": result.error,
            }
        return {
            "status": "running",
            "active": True,
            "sandbox_id": sandbox_id,
        }
    except Exception as e:
        return {
            "status": "terminated",
            "active": False,
            "sandbox_id": sandbox_id,
            "error": str(e),
        }


def kill_sandbox(sandbox_id: str) -> dict:
    """Kill a running sandbox.

    Args:
        sandbox_id: The E2B sandbox ID

    Returns:
        dict with status and sandbox_id
    """
    try:
        sandbox = Sandbox.reconnect(sandbox_id)
        sandbox.kill()
        return {
            "status": "killed",
            "sandbox_id": sandbox_id,
        }
    except Exception as e:
        return {
            "status": "error",
            "sandbox_id": sandbox_id,
            "error": str(e),
        }
