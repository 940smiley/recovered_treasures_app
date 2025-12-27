import uuid
from fastapi import APIRouter
from ..models.schemas import TaskCreate, Run

router = APIRouter()
RUNS: dict[str, Run] = {}

@router.post("")
async def create_task(task: TaskCreate):
    run_id = str(uuid.uuid4())
    run = Run(id=run_id, type=task.type, status="queued", result=None)
    RUNS[run_id] = run
    # TODO: enqueue background job based on task.type
    return {"id": run_id}

@router.get("/{run_id}")
async def get_run(run_id: str):
    return RUNS.get(run_id)
