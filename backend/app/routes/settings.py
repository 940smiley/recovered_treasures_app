from fastapi import APIRouter
from ..db.session import get_session
from ..models.settings import Settings

router = APIRouter()

@router.get('/settings')
async def get_settings():
    with get_session() as session:
        s = session.get(Settings, 1)
        if not s:
            s = Settings()
            session.add(s); session.commit(); session.refresh(s)
        return s

@router.put('/settings')
async def put_settings(payload: dict):
    with get_session() as session:
        s = session.get(Settings, 1)
        if not s:
            s = Settings()
        if 'image_weight' in payload:
            s.image_weight = int(payload['image_weight'])
        if 'recency_weight' in payload:
            s.recency_weight = int(payload['recency_weight'])
        session.add(s); session.commit(); session.refresh(s)
        return s
