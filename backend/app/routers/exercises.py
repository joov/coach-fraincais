from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..database import get_session
from ..models import Lesson, User
from ..services.exercise_evaluator import (
    evaluate_fill_blank,
    evaluate_multiple_choice,
    evaluate_reorder,
    evaluate_match,
    record_result,
)

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


class AnswerRequest(BaseModel):
    exercise_type: str
    register: str  # formal | informal
    exercise_index: int
    # Different answer formats depending on type
    answer_text: str | None = None
    answer_list: list[str] | None = None
    answer_index: int | None = None
    answer_order: list[int] | None = None
    answer_pairs: list[dict] | None = None


@router.get("/{lesson_id}")
async def get_exercises(lesson_id: int, session: Session = Depends(get_session)):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {"lesson_id": lesson_id, "exercises": lesson.exercises}


@router.post("/{lesson_id}/answer")
async def submit_answer(
    lesson_id: int,
    req: AnswerRequest,
    session: Session = Depends(get_session),
):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    user = session.exec(select(User)).first()
    if not user:
        raise HTTPException(status_code=400, detail="No user profile found")

    exercises = lesson.exercises or []
    if req.exercise_index >= len(exercises):
        raise HTTPException(status_code=400, detail="Exercise index out of range")

    exercise = exercises[req.exercise_index]
    evaluation = {}
    is_correct = False
    user_answer_str = ""
    correct_answer_str = ""

    if req.exercise_type == "fill_blank":
        correct = exercise.get("answers", [])
        user_ans = req.answer_list or []
        evaluation = evaluate_fill_blank(user_ans, correct)
        is_correct = evaluation["is_correct"]
        user_answer_str = "|".join(user_ans)
        correct_answer_str = "|".join(correct)

    elif req.exercise_type == "multiple_choice":
        correct_idx = exercise.get("correct_index", 0)
        evaluation = evaluate_multiple_choice(req.answer_index or 0, correct_idx)
        is_correct = evaluation["is_correct"]
        user_answer_str = str(req.answer_index)
        correct_answer_str = str(correct_idx)

    elif req.exercise_type == "reorder":
        correct_order = exercise.get("correct_order", [])
        user_order = req.answer_order or []
        evaluation = evaluate_reorder(user_order, correct_order)
        is_correct = evaluation["is_correct"]
        user_answer_str = str(user_order)
        correct_answer_str = str(correct_order)

    elif req.exercise_type == "match":
        correct_pairs = exercise.get("pairs", [])
        user_pairs = req.answer_pairs or []
        evaluation = evaluate_match(user_pairs, correct_pairs)
        is_correct = evaluation["is_correct"]
        user_answer_str = str(user_pairs)
        correct_answer_str = str(correct_pairs)

    elif req.exercise_type in ("free_answer", "transform"):
        user_answer_str = req.answer_text or ""
        correct_answer_str = ""
        is_correct = True  # Will be evaluated by LLM in a future pass
        evaluation = {"is_correct": True, "note": "Free-form answer recorded."}

    record_result(
        session=session,
        user_id=user.id,
        lesson_id=lesson_id,
        exercise_type=req.exercise_type,
        register=req.register,
        user_answer=user_answer_str,
        correct_answer=correct_answer_str,
        is_correct=is_correct,
    )

    # Stufenweise Fehlerkorrektur
    hint = None
    if not is_correct:
        hint = _generate_hint(exercise, req.exercise_type)

    return {
        "is_correct": is_correct,
        "evaluation": evaluation,
        "hint": hint,
    }


def _generate_hint(exercise: dict, exercise_type: str) -> str | None:
    """Generate a hint without revealing the answer (first attempt)."""
    hints = {
        "fill_blank": "Attention aux mots proposés. Relisez le contexte du dialogue.",
        "multiple_choice": "Réfléchissez au contexte de la situation. Qui parle à qui ?",
        "reorder": "Pensez à l'ordre logique d'une conversation. Qui commence ?",
        "match": "Attention au registre : tu = informel, vous = formel.",
        "transform": "Pensez à changer le pronom et la conjugaison du verbe.",
    }
    return hints.get(exercise_type, "Essayez encore une fois.")
