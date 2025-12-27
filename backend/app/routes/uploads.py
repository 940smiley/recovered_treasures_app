from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from sqlmodel import select
from ..db.session import get_session
from ..models.entities import Item, Image, Draft
from ..storage.files import save_image

router = APIRouter()

@router.post('/items/upload')
async def upload_items(files: List[UploadFile] = File(...), title: Optional[str] = Form(None), category: Optional[str] = Form(None)):
    saved = []
    with get_session() as session:
        item = Item(title=title or None, category=category or None)
        session.add(item)
        session.commit(); session.refresh(item)
        for uf in files:
            content = await uf.read()
            rel_path, file_hash = save_image(uf.filename, content)
            img = Image(item_id=item.id, file_path=rel_path, file_hash=file_hash)
            session.add(img); session.commit(); session.refresh(img)
            saved.append({ 'id': img.id, 'file_path': img.file_path })
        draft = Draft(item_id=item.id, title=item.title or (files[0].filename if files else None), category=item.category)
        session.add(draft); session.commit(); session.refresh(draft)
        return { 'item_id': item.id, 'draft_id': draft.id, 'images': saved }
