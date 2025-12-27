from fastapi import APIRouter, HTTPException

from ..models.ai import GenerationRequest
from ..services import ai

router = APIRouter()


@router.get("/ai/models")
async def available_models():
    return {"models": ai.list_models()}


@router.post("/ai/generate")
async def generate_text(payload: GenerationRequest):
    try:
        return await ai.generate(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
