from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price_suggested: Optional[float] = None
    hotness_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    images: list["Image"] = Relationship(back_populates="item")
    drafts: list["Draft"] = Relationship(back_populates="item")

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    file_path: str
    file_hash: str
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    item: Optional[Item] = Relationship(back_populates="images")

class Draft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    state: str = Field(default="draft")  # draft|pending|listed
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    item: Optional[Item] = Relationship(back_populates="drafts")

class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    platform: str = Field(default="ebay")
    status: str = Field(default="draft")
    listing_id: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
