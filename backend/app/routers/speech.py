import re
import unicodedata

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..services.pronunciation import transcribe_audio, evaluate_pronunciation
from ..services.exercise_evaluator import record_result

router = APIRouter(prefix="/api/speech", tags=["speech"])


def _normalize(text: str) -> str:
    """Lowercase, strip accents, remove punctuation for comparison."""
    text = text.lower().strip()
    # Decompose unicode and remove combining chars (accents)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Replace hyphens with spaces (allez-vous -> allez vous)
    text = text.replace("-", " ")
    # Remove remaining punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _compare_words(target: str, spoken: str) -> dict:
    """Word-by-word comparison between target and spoken text.

    Returns per-word match info and an overall score (0-100).
    """
    target_norm = _normalize(target)
    spoken_norm = _normalize(spoken)

    target_words = target_norm.split()
    spoken_words = spoken_norm.split()

    if not target_words:
        return {"score": 100 if not spoken_words else 0, "words": [], "target_text": target, "spoken_text": spoken}

    # Build match list using a simple greedy alignment
    word_results = []
    spoken_idx = 0
    matched = 0

    for tw in target_words:
        found = False
        # Look for this word in the remaining spoken words (allow small lookahead)
        for offset in range(min(3, len(spoken_words) - spoken_idx)):
            check_idx = spoken_idx + offset
            if check_idx < len(spoken_words) and spoken_words[check_idx] == tw:
                word_results.append({"word": tw, "match": True, "spoken": spoken_words[check_idx]})
                spoken_idx = check_idx + 1
                matched += 1
                found = True
                break
        if not found:
            # Check if word is at least a partial match (first 3+ chars)
            partial = False
            for offset in range(min(3, len(spoken_words) - spoken_idx)):
                check_idx = spoken_idx + offset
                if check_idx < len(spoken_words) and len(tw) >= 3 and spoken_words[check_idx].startswith(tw[:3]):
                    word_results.append({"word": tw, "match": False, "spoken": spoken_words[check_idx], "partial": True})
                    spoken_idx = check_idx + 1
                    matched += 0.5
                    partial = True
                    break
            if not partial:
                word_results.append({"word": tw, "match": False, "spoken": None})

    score = round((matched / len(target_words)) * 100)

    return {
        "score": score,
        "words": word_results,
        "target_text": target,
        "spoken_text": spoken,
        "target_word_count": len(target_words),
        "matched_words": int(matched),
    }


@router.post("/transcribe")
async def transcribe_and_evaluate(
    file: UploadFile = File(...),
    target_text: str = Form(...),
    lesson_id: int = Form(...),
    register: str = Form(default="informal"),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User)).first()
    level = user.current_level if user else "A1"

    # Step 1: Transcribe audio via Whisper
    audio_bytes = await file.read()
    transcription_result = await transcribe_audio(audio_bytes, file.filename or "audio.webm")

    transcribed_text = transcription_result.get("text", "")
    confidence = transcription_result.get("language_probability", 0.0)

    # Step 2: Word-by-word comparison (fast, local, no LLM needed)
    comparison = _compare_words(target_text, transcribed_text)

    # Step 3: LLM evaluation for detailed feedback (only if there were issues)
    evaluation = {}
    if comparison["score"] < 100:
        try:
            evaluation = await evaluate_pronunciation(
                target_text=target_text,
                transcription=transcribed_text,
                confidence=confidence,
                level=level,
            )
        except Exception:
            evaluation = {}

    # Step 4: Record result
    is_correct = comparison["score"] >= 80
    if user:
        record_result(
            session=session,
            user_id=user.id,
            lesson_id=lesson_id,
            exercise_type="dialogue",
            register=register,
            user_answer=transcribed_text,
            correct_answer=target_text,
            is_correct=is_correct,
        )

    return {
        "transcription": transcribed_text,
        "segments": transcription_result.get("segments", []),
        "comparison": comparison,
        "evaluation": evaluation,
    }
