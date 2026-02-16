import logging

from sqlmodel import Session

from ..models import ExerciseResult, ErrorLog

logger = logging.getLogger(__name__)


def evaluate_fill_blank(user_answers: list[str], correct_answers: list[str]) -> dict:
    """Evaluate a fill-in-the-blank exercise."""
    results = []
    all_correct = True
    for i, (user, correct) in enumerate(zip(user_answers, correct_answers)):
        is_match = user.strip().lower() == correct.strip().lower()
        if not is_match:
            all_correct = False
        results.append({
            "index": i,
            "user_answer": user,
            "correct_answer": correct,
            "is_correct": is_match,
        })
    return {"is_correct": all_correct, "details": results}


def evaluate_multiple_choice(selected_index: int, correct_index: int) -> dict:
    """Evaluate a multiple choice exercise."""
    return {
        "is_correct": selected_index == correct_index,
        "selected": selected_index,
        "correct": correct_index,
    }


def evaluate_reorder(user_order: list[int], correct_order: list[int]) -> dict:
    """Evaluate a reorder exercise."""
    return {
        "is_correct": user_order == correct_order,
        "user_order": user_order,
        "correct_order": correct_order,
    }


def evaluate_match(user_pairs: list[dict], correct_pairs: list[dict]) -> dict:
    """Evaluate a matching exercise."""
    correct_map = {p["informal"]: p["formal"] for p in correct_pairs}
    results = []
    all_correct = True
    for pair in user_pairs:
        expected = correct_map.get(pair.get("informal", ""), "")
        is_match = pair.get("formal", "").strip().lower() == expected.strip().lower()
        if not is_match:
            all_correct = False
        results.append({
            "informal": pair.get("informal", ""),
            "user_formal": pair.get("formal", ""),
            "correct_formal": expected,
            "is_correct": is_match,
        })
    return {"is_correct": all_correct, "details": results}


def record_result(
    session: Session,
    user_id: int,
    lesson_id: int,
    exercise_type: str,
    register: str,
    user_answer: str,
    correct_answer: str,
    is_correct: bool,
    attempt: int = 1,
) -> ExerciseResult:
    """Record an exercise result and log errors."""
    result = ExerciseResult(
        user_id=user_id,
        lesson_id=lesson_id,
        exercise_type=exercise_type,
        register=register,
        user_answer=user_answer,
        correct_answer=correct_answer,
        is_correct=is_correct,
        attempt_number=attempt,
    )
    session.add(result)

    if not is_correct:
        # Determine error category
        category = "grammar"
        if exercise_type == "dialogue":
            category = "pronunciation"
        elif exercise_type in ("match", "transform"):
            category = "register"

        error = ErrorLog(
            user_id=user_id,
            lesson_id=lesson_id,
            exercise_type=exercise_type,
            error_category=category,
            error_detail=f"Expected: {correct_answer}, Got: {user_answer}",
            register=register,
        )
        session.add(error)

    session.commit()
    session.refresh(result)
    return result
