from typing import Optional
from sqlmodel import SQLModel, Field

class Settings(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    image_weight: int = 5
    recency_weight: int = 30
