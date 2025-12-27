from fastapi import APIRouter, Query
from ..services.pricing import get_stub_comps

router = APIRouter()

@router.get('/pricing/comps')
async def comps(query: str = Query('')):
    return { 'query': query, 'comps': get_stub_comps(query or 'item') }
