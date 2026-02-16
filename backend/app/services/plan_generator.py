import json
import logging

from sqlmodel import Session, select

from ..models import TrainingPlan, PlanLesson, Lesson
from ..prompts.plan import PLAN_SYSTEM_PROMPT
from . import llm

logger = logging.getLogger(__name__)


async def generate_plan(
    session: Session,
    user_id: int,
    current_level: str,
    target_level: str,
    grammar_focus: list[str],
    topic_focus: list[str],
    minutes_per_day: int,
    days_per_week: int,
) -> TrainingPlan:
    """Generate a personalized training plan using the LLM."""

    user_message = json.dumps(
        {
            "current_level": current_level,
            "target_level": target_level,
            "grammar_focus": grammar_focus,
            "topic_focus": topic_focus,
            "time_budget": {
                "minutes_per_day": minutes_per_day,
                "days_per_week": days_per_week,
            },
        }
    )

    plan_data = await llm.chat_json(PLAN_SYSTEM_PROMPT, user_message)

    # Persist the plan
    plan = TrainingPlan(
        user_id=user_id,
        target_level=target_level,
        grammar_focus=grammar_focus,
        topic_focus=topic_focus,
        time_budget={"minutes_per_day": minutes_per_day, "days_per_week": days_per_week},
        plan_data=plan_data,
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)

    # Create plan_lesson entries and auto-generate lesson stubs
    weeks = plan_data.get("weeks", [])
    order = 0
    for week in weeks:
        for lesson_info in week.get("lessons", []):
            lesson_num = lesson_info.get("lesson_number", 0)

            # Find or create the lesson
            lesson = session.exec(
                select(Lesson).where(Lesson.number == lesson_num)
            ).first()

            if not lesson:
                lesson = Lesson(
                    number=lesson_num,
                    title=lesson_info.get("title", f"Leçon {lesson_num}"),
                    topic=lesson_info.get("title", ""),
                    grammar_focus=lesson_info.get("extra_practice", "") or "",
                    level=current_level,
                    block=(lesson_num - 1) // 9 + 1,
                )
                session.add(lesson)
                session.commit()
                session.refresh(lesson)

            pl = PlanLesson(
                plan_id=plan.id,
                lesson_id=lesson.id,
                order_index=order,
                status="pending",
            )
            session.add(pl)
            order += 1

    session.commit()
    session.refresh(plan)
    return plan
