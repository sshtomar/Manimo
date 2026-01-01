"""Main Modal app definition for Manimo notebooks."""

import modal
from pathlib import Path

# Image with Manim and Marimo
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

