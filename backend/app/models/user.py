from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, JSON, Column


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="")
    current_level: str = Field(default="A1")
    target_level: str = Field(default="A2")
    settings: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
