from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Chapter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    version: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = False  # Fixed typo here
