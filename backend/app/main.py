from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import apps, tasks, uploads, drafts, pricing, jobs, settings, ai
from .db.session import init_db
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="eBay Seller Dashboard API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(apps.router, prefix="/api/apps", tags=["apps"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(uploads.router, prefix="/api", tags=["uploads"])
app.include_router(drafts.router, prefix="/api", tags=["drafts"])
app.include_router(pricing.router, prefix="/api", tags=["pricing"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
app.include_router(settings.router, prefix="/api", tags=["settings"])
app.include_router(ai.router, prefix="/api", tags=["ai"])

@app.get("/api/health")
async def health():
    return {"ok": True}

# Serve images under /storage
storage_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'storage'))
if not os.path.exists(storage_root):
    os.makedirs(storage_root, exist_ok=True)
app.mount("/storage", StaticFiles(directory=storage_root), name="storage")

