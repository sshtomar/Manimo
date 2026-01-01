"""API request and response models."""

from pydantic import BaseModel, Field
from typing import Any


class AskAIRequest(BaseModel):
    """Request for AI assistance."""

    notebook_id: str
    user_id: str
    last_user_prompt: str
    apply: bool = False


class AskAIResponse(BaseModel):
    """Response from AI assistance."""

    patch_type: str  # "cell" | "diff" | "markdown"
    artifact: str
    applied_version_key: str | None = None
    rationale: str | None = None
    discussion_history: list[dict[str, Any]] | None = Field(
        default=None,
        description="Multi-round discussion history (only in iterative mode)"
    )


class RenderVideoRequest(BaseModel):
    """Request to render a video from notebook."""

    notebook_id: str
    user_id: str
    scene_name: str | None = None  # Specific scene to render, or None for all
    quality: str = "medium"  # "low" | "medium" | "high" | "production"
    format: str = "mp4"  # "mp4" | "mov" | "gif"


class RenderVideoResponse(BaseModel):
    """Response from video rendering request."""

    job_id: str
    status: str
    video_url: str | None = None


class GetNotebookRequest(BaseModel):
    """Request to get notebook."""

    notebook_id: str
    user_id: str


class SaveNotebookRequest(BaseModel):
    """Request to save notebook."""

    notebook_id: str
    user_id: str
    content: str


class ListVideosRequest(BaseModel):
    """Request to list rendered videos."""

    notebook_id: str
    user_id: str

