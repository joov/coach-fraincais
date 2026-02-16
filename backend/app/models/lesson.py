from typing import Optional

from sqlmodel import Field, SQLModel, JSON, Column


class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(index=True)
    title: str
    topic: str
    grammar_focus: str = Field(default="")
    level: str = Field(default="A1")
    block: int = Field(default=1)
    dialogues: dict = Field(default_factory=dict, sa_column=Column(JSON))
    exercises: list = Field(default_factory=list, sa_column=Column(JSON))
    grammar_box: dict = Field(default_factory=dict, sa_column=Column(JSON))
