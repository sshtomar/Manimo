"""Notebook CRUD endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models.requests import GetNotebookRequest, SaveNotebookRequest
from ..storage.r2 import (
    get_notebook_content,
    save_notebook_content,
    create_new_notebook,
    list_user_notebooks,
)

router = APIRouter()


class CreateNotebookRequest(BaseModel):
    """Request to create a new notebook."""
    user_id: str = "default"
    title: str | None = None


@router.post("/notebook")
async def create_notebook(request: CreateNotebookRequest):
    """Create a new Marimo notebook and return its ID."""
    try:
        notebook_id = await create_new_notebook(
            user_id=request.user_id,
            title=request.title,
        )

        return {
            "notebook_id": notebook_id,
            "status": "created",
            "url": f"/notebook/{notebook_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notebook: {e}")


@router.get("/notebook/{notebook_id}")
async def get_notebook(notebook_id: str, user_id: str = "default"):
    """Get notebook content."""
    try:
        content = await get_notebook_content(notebook_id, user_id)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Notebook not found: {e}")


@router.put("/notebook/{notebook_id}")
async def save_notebook(notebook_id: str, content: str, user_id: str = "default"):
    """Save notebook content."""
    try:
        version_key = await save_notebook_content(notebook_id, user_id, content)
        return {"version_key": version_key, "status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save: {e}")


@router.get("/notebooks")
async def list_notebooks(user_id: str = "default"):
    """List all notebooks for a user."""
    try:
        notebooks = await list_user_notebooks(user_id)
        return {"notebooks": notebooks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list notebooks: {e}")

