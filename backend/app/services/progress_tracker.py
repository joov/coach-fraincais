import json
import logging

from sqlmodel import Session, select, func

from ..models import ExerciseResult, ErrorLog, PlanLesson
from ..prompts.evaluation import ERROR_ANALYSIS_SYSTEM_PROMPT
from . import llm

logger = logging.getLogger(__name__)


def get_progress_summary(session: Session, user_id: int) -> dict:
    """Get a summary of the user's progress."""
    # Total exercises attempted
    total = session.exec(
        select(func.count(ExerciseResult.id)).where(ExerciseResult.user_id == user_id)
    ).one()

    # Correct answers
    correct = session.exec(
        select(func.count(ExerciseResult.id)).where(
            ExerciseResult.user_id == user_id,
            ExerciseResult.is_correct == True,  # noqa: E712
        )
    ).one()

    # Completed lessons
    completed_lessons = session.exec(
        select(func.count(PlanLesson.id)).where(PlanLesson.status == "completed")
    ).one()

    # Total planned lessons
    total_lessons = session.exec(
        select(func.count(PlanLesson.id))
    ).one()

    # Error counts by category
    error_counts = {}
    errors = session.exec(
        select(ErrorLog.error_category, func.count(ErrorLog.id))
        .where(ErrorLog.user_id == user_id)
        .group_by(ErrorLog.error_category)
    ).all()
    for category, count in errors:
        error_counts[category] = count

    return {
        "total_exercises": total,
        "correct_answers": correct,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "error_counts": error_counts,
    }


async def get_error_analysis(session: Session, user_id: int, level: str) -> dict:
    """Get a detailed error analysis using the LLM."""
    errors = session.exec(
        select(ErrorLog).where(ErrorLog.user_id == user_id).order_by(ErrorLog.created_at.desc()).limit(100)  # type: ignore
    ).all()

    if not errors:
        return {
            "top_errors": [],
            "level_assessment": {
                "grammar": level,
                "vocabulary": level,
                "pronunciation": level,
                "comprehension": level,
                "overall": level,
                "trend": "stable",
            },
            "recommendations": ["Continue with the current lesson plan."],
        }

    error_data = [
        {
            "category": e.error_category,
            "detail": e.error_detail,
            "exercise_type": e.exercise_type,
            "register": e.register,
            "lesson_id": e.lesson_id,
        }
        for e in errors
    ]

    system_prompt = ERROR_ANALYSIS_SYSTEM_PROMPT.format(
        level=level,
        errors=json.dumps(error_data),
    )
    user_message = f"Analyze the error history for a {level} student."

    result = await llm.chat_json(system_prompt, user_message)
    return result
