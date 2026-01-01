"""Storage package."""

from .r2 import (
    get_notebook_content,
    save_notebook_content,
    create_new_notebook,
    list_user_notebooks,
    list_notebook_videos,
    get_video_url,
    upload_video,
)

__all__ = [
    "get_notebook_content",
    "save_notebook_content",
    "create_new_notebook",
    "list_user_notebooks",
    "list_notebook_videos",
    "get_video_url",
    "upload_video",
]
