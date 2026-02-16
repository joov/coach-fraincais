from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ..database import get_session
from ..models import TrainingPlan, PlanLesson, Lesson, User
from ..services.plan_generator import generate_plan

router = APIRouter(prefix="/api/plan", tags=["plan"])


class PlanCreateRequest(BaseModel):
    target_level: str
    grammar_focus: list[str] = []
    topic_focus: list[str] = []
    minutes_per_day: int = 20
    days_per_week: int = 3


@router.post("")
async def create_plan(req: PlanCreateRequest, session: Session = Depends(get_session)):
    # Get or create user
    user = session.exec(select(User)).first()
    if not user:
        user = User(name="Learner", current_level="A1", target_level=req.target_level)
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        user.target_level = req.target_level
        session.add(user)
        session.commit()

    plan = await generate_plan(
        session=session,
        user_id=user.id,
        current_level=user.current_level,
        target_level=req.target_level,
        grammar_focus=req.grammar_focus,
        topic_focus=req.topic_focus,
        minutes_per_day=req.minutes_per_day,
        days_per_week=req.days_per_week,
    )

    return {
        "id": plan.id,
        "target_level": plan.target_level,
        "grammar_focus": plan.grammar_focus,
        "topic_focus": plan.topic_focus,
        "time_budget": plan.time_budget,
        "plan": plan.plan_data,
    }


@router.get("")
async def get_plan(session: Session = Depends(get_session)):
    plan = session.exec(
        select(TrainingPlan).order_by(TrainingPlan.created_at.desc())  # type: ignore
    ).first()

    if not plan:
        return {"plan": None}

    return {
        "id": plan.id,
        "target_level": plan.target_level,
        "grammar_focus": plan.grammar_focus,
        "topic_focus": plan.topic_focus,
        "time_budget": plan.time_budget,
        "plan": plan.plan_data,
    }


BLOCK_NAMES = {
    1: "Bloc 1 – Premiers contacts",
    2: "Bloc 2 – Temps, météo et métier",
    3: "Bloc 3 – En ville",
    4: "Bloc 4 – Courses et repas",
    5: "Bloc 5 – Santé et administration",
    6: "Bloc 6 – Shopping et loisirs",
    7: "Bloc 7 – Voyages et urgences",
}


@router.get("/lessons")
async def get_plan_lessons(session: Session = Depends(get_session)):
    """Return the ordered list of lessons from the current plan, with their status."""
    plan = session.exec(
        select(TrainingPlan).order_by(TrainingPlan.created_at.desc())  # type: ignore
    ).first()

    if not plan:
        return []

    # First try: plan_lesson entries in the DB (created when plan_data was valid)
    plan_lessons = session.exec(
        select(PlanLesson).where(PlanLesson.plan_id == plan.id).order_by(PlanLesson.order_index)
    ).all()

    result = []
    for pl in plan_lessons:
        lesson = session.get(Lesson, pl.lesson_id)
        if lesson:
            result.append({
                "id": lesson.id,
                "number": lesson.number,
                "title": lesson.title,
                "topic": lesson.topic,
                "grammar_focus": lesson.grammar_focus,
                "level": lesson.level,
                "block": lesson.block,
                "block_name": BLOCK_NAMES.get(lesson.block, f"Bloc {lesson.block}"),
                "status": pl.status,
                "has_content": bool(lesson.dialogues and lesson.dialogues.get("informal")),
                "order_index": pl.order_index,
            })

    # Fallback: build list from plan_data.weeks (when plan_lessons were not created)
    if not result and plan.plan_data:
        weeks = plan.plan_data.get("weeks", [])
        idx = 0
        for week in weeks:
            for lesson_info in week.get("lessons", []):
                num = lesson_info.get("lesson_number", 0)
                block = (num - 1) // 9 + 1 if num > 0 else 0
                result.append({
                    "id": None,
                    "number": num,
                    "title": lesson_info.get("title", f"Leçon {num}"),
                    "topic": lesson_info.get("title", ""),
                    "grammar_focus": lesson_info.get("extra_practice") or "",
                    "level": plan.target_level,
                    "block": block,
                    "block_name": BLOCK_NAMES.get(block, f"Bloc {block}"),
                    "status": "pending",
                    "has_content": False,
                    "order_index": idx,
                    "is_priority": lesson_info.get("is_priority", False),
                })
                idx += 1

    return result
