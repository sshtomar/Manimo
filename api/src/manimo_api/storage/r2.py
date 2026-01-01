"""R2 / S3-compatible storage client for Manimo (with video support)."""

import boto3
import json
import uuid
from datetime import datetime
from ..config import settings
from ..utils import generate_notebook_name, generate_notebook_title


def get_r2_client():
    """Get boto3 S3 client configured for Cloudflare R2."""
    return boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def get_notebook_key(notebook_id: str, user_id: str) -> str:
    """Get the S3 key for a notebook."""
    return f"{user_id}/{notebook_id}/notebook.py"


async def get_notebook_content(notebook_id: str, user_id: str) -> str:
    """Get notebook content from R2."""
    client = get_r2_client()
    key = get_notebook_key(notebook_id, user_id)

    try:
        response = client.get_object(Bucket=settings.R2_BUCKET, Key=key)
        return response["Body"].read().decode("utf-8")
    except client.exceptions.NoSuchKey:
        # Return empty Marimo template for Manim
        return """import marimo

app = marimo.App()

@app.cell
def __():
    import marimo as mo
    return mo.md(\"\"\"
# New Animation

Start creating your Manim animation here. Ask the AI assistant for help!
\"\"\"),

@app.cell
def create_scene():
    from manim import *
    
    # Create your scene here
    # Example: class MyScene(Scene): ...
    return ()
"""


async def save_notebook_content(notebook_id: str, user_id: str, content: str) -> str:
    """Save notebook content to R2."""
    client = get_r2_client()
    key = get_notebook_key(notebook_id, user_id)

    client.put_object(
        Bucket=settings.R2_BUCKET,
        Key=key,
        Body=content.encode("utf-8"),
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    version_key = f"{user_id}/{notebook_id}/versions/notebook-{timestamp}.py"
    client.put_object(
        Bucket=settings.R2_BUCKET,
        Key=version_key,
        Body=content.encode("utf-8"),
    )

    return version_key


async def list_notebook_videos(notebook_id: str, user_id: str) -> list[dict]:
    """List rendered video files for a notebook."""
    client = get_r2_client()
    prefix = f"{user_id}/{notebook_id}/videos/"

    try:
        response = client.list_objects_v2(
            Bucket=settings.R2_BUCKET,
            Prefix=prefix,
        )

        if "Contents" not in response:
            return []

        videos = []
        for obj in response["Contents"]:
            key = obj["Key"]
            filename = key.split("/")[-1]
            videos.append({
                "key": key,
                "filename": filename,
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
            })

        return sorted(videos, key=lambda x: x["last_modified"], reverse=True)
    except Exception:
        return []


async def upload_video(notebook_id: str, user_id: str, video_path: str, video_filename: str) -> str:
    """Upload a rendered video to R2."""
    client = get_r2_client()
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    video_key = f"{user_id}/{notebook_id}/videos/{timestamp}-{video_filename}"

    with open(video_path, "rb") as f:
        client.upload_fileobj(
            f,
            Bucket=settings.R2_BUCKET,
            Key=video_key,
            ExtraArgs={"ContentType": "video/mp4"},
        )

    return video_key


async def get_video_url(notebook_id: str, user_id: str, video_key: str, expires_in: int = 3600) -> str:
    """Generate a presigned URL for a video."""
    client = get_r2_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.R2_BUCKET, "Key": video_key},
        ExpiresIn=expires_in,
    )
    return url


async def create_new_notebook(user_id: str, title: str | None = None) -> str:
    """Create a new notebook with a memorable name."""
    notebook_id = generate_notebook_name()

    if not title:
        title = generate_notebook_title(notebook_id)

    initial_content = f'''"""
{title}

Created: {datetime.utcnow().isoformat()}
"""

import marimo

app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo.md("""
# {title}

Start creating your Manim animation here. You can ask the AI assistant for help!
"""),


@app.cell
def create_scene():
    from manim import *
    
    # Create your scene here
    # Example:
    # class MyScene(Scene):
    #     def construct(self):
    #         text = Text("Hello, Manim!")
    #         self.play(Write(text))
    return ()
'''

    await save_notebook_content(notebook_id, user_id, initial_content)
    return notebook_id


async def list_user_notebooks(user_id: str) -> list[dict]:
    """List all notebooks for a user."""
    client = get_r2_client()
    prefix = f"{user_id}/"

    try:
        response = client.list_objects_v2(
            Bucket=settings.R2_BUCKET,
            Prefix=prefix,
            Delimiter="/"
        )

        notebooks = []
        if "CommonPrefixes" in response:
            for prefix_obj in response["CommonPrefixes"]:
                notebook_id = prefix_obj["Prefix"].rstrip("/").split("/")[-1]

                try:
                    key = f"{user_id}/{notebook_id}/notebook.py"
                    obj_info = client.head_object(Bucket=settings.R2_BUCKET, Key=key)
                    content = client.get_object(Bucket=settings.R2_BUCKET, Key=key)["Body"].read().decode("utf-8")
                    title, created_at = _extract_notebook_metadata(content, notebook_id)

                    notebooks.append({
                        "notebook_id": notebook_id,
                        "title": title,
                        "created_at": created_at or obj_info["LastModified"].isoformat(),
                        "updated_at": obj_info["LastModified"].isoformat(),
                    })
                except Exception:
                    continue

        return sorted(notebooks, key=lambda x: x["updated_at"], reverse=True)
    except Exception:
        return []


def _extract_notebook_metadata(content: str, notebook_id: str) -> tuple[str, str | None]:
    """Extract title and creation date from notebook content."""
    lines = content.split("\n")
    title = None
    created_at = None

    if len(lines) > 1 and lines[0].startswith('"""'):
        if len(lines) > 1:
            title = lines[1].strip()

        for i, line in enumerate(lines[2:10], start=2):
            if line.startswith("Created:"):
                try:
                    created_at = line.split("Created:", 1)[1].strip()
                except Exception:
                    pass
                break

    if not title:
        title = generate_notebook_title(notebook_id)

    return title, created_at

