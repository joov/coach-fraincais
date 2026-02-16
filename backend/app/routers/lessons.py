from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Lesson, User, PlanLesson
from ..services.lesson_generator import generate_lesson_content, generate_exercises

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("")
async def list_lessons(session: Session = Depends(get_session)):
    lessons = session.exec(select(Lesson).order_by(Lesson.number)).all()
    return [
        {
            "id": l.id,
            "number": l.number,
            "title": l.title,
            "topic": l.topic,
            "grammar_focus": l.grammar_focus,
            "level": l.level,
            "block": l.block,
            "has_content": bool(l.dialogues and l.dialogues.get("informal")),
        }
        for l in lessons
    ]


@router.get("/{lesson_id}")
async def get_lesson(lesson_id: int, session: Session = Depends(get_session)):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Auto-generate content if missing
    user = session.exec(select(User)).first()
    level = user.current_level if user else "A1"

    if not lesson.dialogues or not lesson.dialogues.get("informal"):
        lesson = await generate_lesson_content(session, lesson, level)

    if not lesson.exercises:
        lesson = await generate_exercises(session, lesson, level)

    return {
        "id": lesson.id,
        "number": lesson.number,
        "title": lesson.title,
        "topic": lesson.topic,
        "grammar_focus": lesson.grammar_focus,
        "level": lesson.level,
        "block": lesson.block,
        "dialogues": lesson.dialogues,
        "exercises": lesson.exercises,
        "grammar_box": lesson.grammar_box,
    }


@router.post("/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, session: Session = Depends(get_session)):
    """Mark a lesson as completed in the current plan."""
    plan_lesson = session.exec(
        select(PlanLesson).where(PlanLesson.lesson_id == lesson_id)
    ).first()

    if plan_lesson:
        plan_lesson.status = "completed"
        session.add(plan_lesson)
        session.commit()

    return {"status": "ok"}
