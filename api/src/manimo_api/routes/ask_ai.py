"""AI assistance endpoint."""

from fastapi import APIRouter, HTTPException
from ..models.requests import AskAIRequest, AskAIResponse
from ..generation.orchestrator import orchestrate_generation

router = APIRouter()


@router.post("/ask_ai", response_model=AskAIResponse)
async def ask_ai(request: AskAIRequest) -> AskAIResponse:
    """
    Generate Manim animation code using skills-based approach with mandatory compliance.

    Two-pass generation:
    1. Analyzes the task and selects relevant skills
    2. Generates rigorous code following ALL skill requirements
    3. Includes built-in self-validation

    Returns a proposed patch (cell or diff) and optionally applies it.
    """
    try:
        result = await orchestrate_generation(
            notebook_id=request.notebook_id,
            user_id=request.user_id,
            user_prompt=request.last_user_prompt,
            apply=request.apply,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

