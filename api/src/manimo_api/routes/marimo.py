"""Marimo session management endpoints."""

import modal
import logfire
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


class LaunchMarimoRequest(BaseModel):
    """Request to launch a Marimo editing session."""
    notebook_id: str
    user_id: str = "default"


class LaunchMarimoResponse(BaseModel):
    """Response from launching a Marimo session."""
    notebook_id: str
    url: str
    status: str
    sandbox_id: str | None = None


@router.post("/marimo/launch", response_model=LaunchMarimoResponse)
async def launch_marimo_session(request: LaunchMarimoRequest) -> LaunchMarimoResponse:
    """
    Launch an interactive Marimo editing session in a Modal sandbox.

    This endpoint:
    1. Creates an isolated Modal sandbox with Marimo installed
    2. Downloads the notebook from R2 storage
    3. Starts the Marimo edit server with AI configuration
    4. Returns a tunnel URL for browser access

    The sandbox includes:
    - In-sandbox Agent SDK server on port 8081 for AI assistance
    - Auto-sync to R2 every 5 seconds
    - 30-minute idle timeout
    """
    with logfire.span(
        "marimo.launch",
        notebook_id=request.notebook_id,
        user_id=request.user_id,
    ):
        logfire.info("Launching Marimo session")

        try:
            # Call the Modal function to spawn the notebook sandbox
            launch_fn = modal.Function.from_name(
                "manimo-notebooks", "spawn_notebook_sandbox"
            )

            result = launch_fn.remote(
                notebook_id=request.notebook_id,
                user_id=request.user_id,
            )

            logfire.info(
                "Marimo session launched",
                url=result["marimo_url"],
                status=result["status"],
            )

            return LaunchMarimoResponse(
                notebook_id=request.notebook_id,
                url=result["marimo_url"],
                status=result["status"],
                sandbox_id=result.get("sandbox_id"),
            )

        except modal.exception.NotFoundError:
            logfire.error("Modal function not found - app may not be deployed")
            raise HTTPException(
                status_code=503,
                detail="Marimo service unavailable. Please ensure the Modal app is deployed.",
            )
        except TimeoutError as e:
            logfire.error("Sandbox creation timed out", error=str(e))
            raise HTTPException(
                status_code=504,
                detail="Sandbox creation timed out. Please try again.",
            )
        except Exception as e:
            logfire.error("Failed to launch Marimo session", error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to launch Marimo: {e}",
            )


@router.get("/marimo/status/{sandbox_id}")
async def get_marimo_status(sandbox_id: str) -> dict:
    """
    Check the status of a running Marimo sandbox.

    Returns the current status and whether the session is still active.
    """
    with logfire.span("marimo.status", sandbox_id=sandbox_id):
        try:
            # Check sandbox status via Modal
            check_fn = modal.Function.from_name(
                "manimo-notebooks", "check_sandbox_status"
            )
            result = check_fn.remote(sandbox_id=sandbox_id)
            return result
        except modal.exception.NotFoundError:
            return {"status": "not_found", "active": False}
        except Exception as e:
            logfire.error("Failed to check sandbox status", error=str(e))
            return {"status": "error", "active": False, "error": str(e)}
