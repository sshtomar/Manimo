"""Marimo session management endpoints."""

import logfire
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from manimo_e2b.sandbox import spawn_notebook_sandbox, check_sandbox_status, kill_sandbox


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
    Launch an interactive Marimo editing session in an E2B sandbox.

    This endpoint:
    1. Creates an isolated E2B sandbox with Marimo installed
    2. Downloads the notebook from R2 storage
    3. Starts the Marimo edit server with AI configuration
    4. Returns a URL for browser access

    The sandbox includes:
    - In-sandbox AI server on port 8081 for AI assistance
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
            # Spawn the E2B sandbox
            result = spawn_notebook_sandbox(
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
            result = check_sandbox_status(sandbox_id=sandbox_id)
            return result
        except Exception as e:
            logfire.error("Failed to check sandbox status", error=str(e))
            return {"status": "error", "active": False, "error": str(e)}


@router.delete("/marimo/sandbox/{sandbox_id}")
async def terminate_marimo_sandbox(sandbox_id: str) -> dict:
    """
    Terminate a running Marimo sandbox.

    Use this to clean up sandboxes that are no longer needed.
    """
    with logfire.span("marimo.kill", sandbox_id=sandbox_id):
        try:
            result = kill_sandbox(sandbox_id=sandbox_id)
            return result
        except Exception as e:
            logfire.error("Failed to kill sandbox", error=str(e))
            return {"status": "error", "sandbox_id": sandbox_id, "error": str(e)}
