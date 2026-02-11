"""Video rendering and management endpoints."""

from fastapi import APIRouter, HTTPException
from ..models.requests import (
    RenderVideoRequest,
    RenderVideoResponse,
    ListVideosRequest,
)
from ..storage.r2 import list_notebook_videos, get_video_url

router = APIRouter()


@router.post("/render", response_model=RenderVideoResponse)
async def render_video(request: RenderVideoRequest) -> RenderVideoResponse:
    """
    Request video rendering from a notebook.

    Triggers E2B sandbox to render Manim scene(s) and upload to R2.
    """
    try:
        # TODO: Implement E2B rendering trigger via manimo_e2b.render
        return RenderVideoResponse(
            job_id="placeholder-job-id",
            status="pending",
            video_url=None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notebook/{notebook_id}/videos")
async def list_videos(notebook_id: str, user_id: str = "default"):
    """List all rendered videos for a notebook."""
    try:
        videos = await list_notebook_videos(notebook_id, user_id)
        return {"videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list videos: {e}")


@router.get("/video/{video_key}/url")
async def get_video_presigned_url(video_key: str, expires_in: int = 3600):
    """Get a presigned URL for a video."""
    try:
        url = await get_video_url("", "", video_key, expires_in)
        return {"url": url, "expires_in": expires_in}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

