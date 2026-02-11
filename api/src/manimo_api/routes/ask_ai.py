"""AI assistance endpoint."""

from fastapi import APIRouter, HTTPException

from ..models.requests import AskAIRequest, AskAIResponse
from ..generation.orchestrator import orchestrate_generation

router = APIRouter()


@router.post("/ask_ai", response_model=AskAIResponse)
async def ask_ai(request: AskAIRequest) -> AskAIResponse:
    """
    Generate Manim animation code.

    Two modes available:
    1. Standard mode (default): Skills-based two-pass generation
    2. Agent mode: Claude Agent SDK in E2B sandbox for autonomous generation

    Returns a proposed patch (cell or diff) and optionally applies it.
    """
    try:
        if request.agent_mode:
            from ..generation.agent_orchestrator import orchestrate_with_agent
            result = await orchestrate_with_agent(
                notebook_id=request.notebook_id,
                user_id=request.user_id,
                user_prompt=request.last_user_prompt,
                apply=request.apply,
                use_subagents=request.use_subagents,
            )
        else:
            result = await orchestrate_generation(
                notebook_id=request.notebook_id,
                user_id=request.user_id,
                user_prompt=request.last_user_prompt,
                apply=request.apply,
            )
        return result
    except TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail=f"Agent execution timed out: {e}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

