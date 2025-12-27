from fastapi import APIRouter
from ..registry import REGISTRY
from ..adapters import anythingllm

router = APIRouter()

@router.get("")
async def list_apps():
    return REGISTRY

@router.get("/ping")
async def ping_all():
    statuses = {}
    statuses["anythingllm"] = await anythingllm.health()
    statuses["api"] = True
    return statuses
