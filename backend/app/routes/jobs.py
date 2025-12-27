from fastapi import APIRouter
from ..services.hotness import recalc_all_hotness

router = APIRouter()

@router.post('/hotness/run')
async def run_hotness():
    updated = recalc_all_hotness()
    return { 'updated': updated }
