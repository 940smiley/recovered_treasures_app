from typing import Optional, List, Any
from pydantic import BaseModel, Field

class ImageOut(BaseModel):
    id: int
    file_path: str

class DraftOut(BaseModel):
    id: int
    item_id: int
    state: str
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    image: Optional[ImageOut] = None

class DraftUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None


class AppInfo(BaseModel):
    """Metadata about an external application exposed by the API."""

    key: str
    name: str
    endpoints: List[str] = Field(default_factory=list)


class TaskCreate(BaseModel):
    """Request payload for creating a background task."""

    type: str


class Run(BaseModel):
    """Represents the status of a background task run."""

    id: str
    type: str
    status: str
    result: Optional[Any] = None
