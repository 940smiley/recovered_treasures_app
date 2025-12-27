import httpx
from ..config import ANYTHINGLLM_BASE_URL, ANYTHINGLLM_API_KEY

async def health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{ANYTHINGLLM_BASE_URL}/v1/system")
            return r.status_code < 500
    except Exception:
        return False

async def list_workspaces():
    headers = {"Authorization": f"Bearer {ANYTHINGLLM_API_KEY}"} if ANYTHINGLLM_API_KEY else {}
    async with httpx.AsyncClient(timeout=10, headers=headers) as client:
        r = await client.get(f"{ANYTHINGLLM_BASE_URL}/v1/workspace")
        r.raise_for_status()
        return r.json()
