import hashlib
import os
from datetime import datetime
from typing import Tuple

STORAGE_ROOT = os.getenv("STORAGE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "images")))

os.makedirs(STORAGE_ROOT, exist_ok=True)

def _hash_bytes(data: bytes) -> str:
    h = hashlib.sha256(); h.update(data); return h.hexdigest()

def save_image(file_name: str, content: bytes) -> Tuple[str, str]:
    file_hash = _hash_bytes(content)
    ext = os.path.splitext(file_name)[1].lower() or ".jpg"
    now = datetime.utcnow()
    subdir = os.path.join(STORAGE_ROOT, str(now.year), f"{now.month:02d}")
    os.makedirs(subdir, exist_ok=True)
    target = os.path.join(subdir, f"{file_hash}{ext}")
    if not os.path.exists(target):
        with open(target, 'wb') as f:
            f.write(content)
    rel = os.path.relpath(target, os.path.join(os.path.dirname(__file__), ".."))
    return rel.replace('\\','/'), file_hash
