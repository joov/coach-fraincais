from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ExerciseResult(SQLModel, table=True):
    __tablename__ = "exercise_result"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    lesson_id: int = Field(foreign_key="lesson.id")
    exercise_type: str  # fill_blank | multiple_choice | reorder | match | free_answer | transform | dialogue
    register: str  # formal | informal
    user_answer: str = ""
    correct_answer: str = ""
    is_correct: bool = False
    attempt_number: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
