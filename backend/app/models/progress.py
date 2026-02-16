from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ErrorLog(SQLModel, table=True):
    __tablename__ = "error_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    lesson_id: int = Field(foreign_key="lesson.id")
    exercise_type: str
    error_category: str  # grammar | vocabulary | pronunciation | register
    error_detail: str = ""
    register: str = ""  # formal | informal
    created_at: datetime = Field(default_factory=datetime.utcnow)
