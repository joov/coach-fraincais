from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, JSON, Column


class TrainingPlan(SQLModel, table=True):
    __tablename__ = "training_plan"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    target_level: str
    grammar_focus: list = Field(default_factory=list, sa_column=Column(JSON))
    topic_focus: list = Field(default_factory=list, sa_column=Column(JSON))
    time_budget: dict = Field(default_factory=dict, sa_column=Column(JSON))
    plan_data: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlanLesson(SQLModel, table=True):
    __tablename__ = "plan_lesson"

    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="training_plan.id")
    lesson_id: int = Field(foreign_key="lesson.id")
    order_index: int
    status: str = Field(default="pending")  # pending | in_progress | completed | skipped
    scheduled_date: Optional[str] = None
