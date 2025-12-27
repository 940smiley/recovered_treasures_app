from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..db.session import get_session
from ..models.entities import Draft, Image
from ..models.schemas import DraftOut, DraftUpdate, ImageOut

router = APIRouter()

@router.get('/drafts')
async def list_drafts() -> list[DraftOut]:
    with get_session() as session:
        drafts = session.exec(select(Draft)).all()
        out = []
        for d in drafts:
            img = session.exec(select(Image).where(Image.item_id == d.item_id)).first()
            out.append(DraftOut(
                id=d.id, item_id=d.item_id, state=d.state, title=d.title, description=d.description, category=d.category, price=d.price,
                image=ImageOut(id=img.id, file_path=img.file_path) if img else None
            ))
        return out

@router.get('/drafts/{draft_id}')
async def get_draft(draft_id: int) -> DraftOut:
    with get_session() as session:
        d = session.get(Draft, draft_id)
        if not d:
            raise HTTPException(status_code=404, detail='Draft not found')
        img = session.exec(select(Image).where(Image.item_id == d.item_id)).first()
        return DraftOut(
            id=d.id, item_id=d.item_id, state=d.state, title=d.title, description=d.description, category=d.category, price=d.price,
            image=ImageOut(id=img.id, file_path=img.file_path) if img else None
        )

@router.put('/drafts/{draft_id}')
async def update_draft(draft_id: int, payload: DraftUpdate) -> dict:
    with get_session() as session:
        d = session.get(Draft, draft_id)
        if not d:
            raise HTTPException(status_code=404, detail='Draft not found')
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(d, k, v)
        session.add(d); session.commit()
        return { 'ok': True }

@router.delete('/drafts/{draft_id}')
async def delete_draft(draft_id: int) -> dict:
    with get_session() as session:
        d = session.get(Draft, draft_id)
        if not d:
            return { 'ok': True }
        session.delete(d); session.commit()
        return { 'ok': True }
