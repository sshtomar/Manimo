"""Manim video rendering in E2B sandboxes.

Note: E2B may not support GPU acceleration. Video rendering will use CPU,
which is slower but functional.
"""

from e2b_code_interpreter import Sandbox

from manimo_e2b.config import settings


def render_manim_video(
    notebook_id: str,
    user_id: str,
    scene_name: str | None = None,
    quality: str = "medium",
) -> dict:
    """
    Render a Manim video from a notebook.

    This creates a temporary sandbox, downloads the notebook, renders the video,
    uploads to R2, and terminates the sandbox.

    Args:
        notebook_id: Notebook ID
        user_id: User ID
        scene_name: Specific scene to render, or None for all scenes
        quality: "low" | "medium" | "high" | "production"

    Returns:
        dict with status, videos (list of R2 keys), or error
    """
    r2_bucket = settings.R2_BUCKET
    notebook_key = f"{user_id}/{notebook_id}/notebook.py"

    # Quality to Manim flag mapping
    quality_map = {
        "low": "low_quality",
        "medium": "medium_quality",
        "high": "high_quality",
        "production": "production_quality",
    }
    quality_flag = quality_map.get(quality, "medium_quality")

    # Create sandbox for rendering
    sandbox = Sandbox(
        template=settings.E2B_TEMPLATE,
        timeout=30 * 60,  # 30 minutes for rendering
        envs={
            "R2_ENDPOINT": settings.R2_ENDPOINT,
            "R2_ACCESS_KEY_ID": settings.R2_ACCESS_KEY_ID,
            "R2_SECRET_ACCESS_KEY": settings.R2_SECRET_ACCESS_KEY,
        },
    )

    try:
        # Download notebook
        download_script = f'''
import os
import boto3

client = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

client.download_file("{r2_bucket}", "{notebook_key}", "/home/user/workspace/notebook.py")
print("Downloaded notebook")
'''
        result = sandbox.commands.run(f"python3 -c '''{download_script}'''")
        if result.error:
            return {"status": "error", "error": f"Download failed: {result.error}"}

        # Find Scene classes in the notebook
        find_scenes_script = '''
import ast
import sys

with open("/home/user/workspace/notebook.py", "r") as f:
    source = f.read()

# Parse the notebook to find Scene subclasses
tree = ast.parse(source)
scenes = []

for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for base in node.bases:
            if isinstance(base, ast.Name) and "Scene" in base.id:
                scenes.append(node.name)
            elif isinstance(base, ast.Attribute) and "Scene" in base.attr:
                scenes.append(node.name)

print("SCENES:" + ",".join(scenes))
'''
        result = sandbox.commands.run(f"python3 -c '''{find_scenes_script}'''")
        if result.error or "SCENES:" not in (result.stdout or ""):
            return {"status": "error", "error": "No Scene classes found in notebook"}

        scenes_line = [line for line in (result.stdout or "").split("\n") if line.startswith("SCENES:")][0]
        scene_classes = [s for s in scenes_line.replace("SCENES:", "").split(",") if s]

        if not scene_classes:
            return {"status": "error", "error": "No Scene classes found in notebook"}

        # Filter to specific scene if requested
        if scene_name:
            if scene_name not in scene_classes:
                return {"status": "error", "error": f"Scene '{scene_name}' not found"}
            scene_classes = [scene_name]

        # Render each scene
        rendered_videos = []
        for scene_class_name in scene_classes:
            print(f"Rendering scene: {scene_class_name}")

            # Render with Manim (CPU, no GPU)
            render_cmd = (
                f"cd /home/user/workspace && "
                f"python3 -m manim render notebook.py {scene_class_name} "
                f"--{quality_flag} "
                f"-o {scene_class_name}.mp4"
            )
            result = sandbox.commands.run(render_cmd, timeout=600)

            if result.error:
                print(f"Render warning for {scene_class_name}: {result.error}")
                continue

            # Find the output video
            find_video_script = f'''
from pathlib import Path
import glob

# Manim outputs to media/videos/notebook/<quality>/
patterns = [
    "/home/user/workspace/media/videos/notebook/*/{scene_class_name}.mp4",
    "/home/user/workspace/{scene_class_name}.mp4",
]

for pattern in patterns:
    matches = glob.glob(pattern)
    if matches:
        print(f"VIDEO:{{matches[0]}}")
        break
'''
            result = sandbox.commands.run(f"python3 -c '''{find_video_script}'''")
            if "VIDEO:" not in (result.stdout or ""):
                print(f"Video not found for {scene_class_name}")
                continue

            video_path = [line for line in (result.stdout or "").split("\n") if line.startswith("VIDEO:")][0].replace("VIDEO:", "")

            # Upload to R2
            video_key = f"{user_id}/{notebook_id}/videos/{scene_class_name}.mp4"
            upload_script = f'''
import os
import boto3

client = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

client.upload_file(
    "{video_path}",
    "{r2_bucket}",
    "{video_key}",
    ExtraArgs={{"ContentType": "video/mp4"}},
)
print("Uploaded video to R2")
'''
            result = sandbox.commands.run(f"python3 -c '''{upload_script}'''")
            if result.error:
                print(f"Upload warning for {scene_class_name}: {result.error}")
                continue

            rendered_videos.append(video_key)

        return {
            "status": "completed",
            "videos": rendered_videos,
        }

    finally:
        # Clean up sandbox
        try:
            sandbox.kill()
        except Exception:
            pass
