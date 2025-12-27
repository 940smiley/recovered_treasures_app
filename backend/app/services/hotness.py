from sqlmodel import select
from ..models.entities import Item
from ..models.settings import Settings
from ..db.session import get_session
from datetime import datetime

def _get_settings(session):
    s = session.get(Settings, 1)
    if not s:
        s = Settings()
        session.add(s); session.commit(); session.refresh(s)
    return s

def recalc_all_hotness() -> int:
    updated = 0
    with get_session() as session:
        cfg = _get_settings(session)
        items = session.exec(select(Item)).all()
        for it in items:
            age_days = max(1, (datetime.utcnow() - it.created_at).days)
            img_count = len(it.images)
            it.hotness_score = max(0.0, (cfg.image_weight * img_count) + (cfg.recency_weight / age_days))
            session.add(it)
            updated += 1
        session.commit()
    return updated
