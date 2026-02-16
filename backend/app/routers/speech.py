from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..services.pronunciation import transcribe_audio, evaluate_pronunciation
from ..services.exercise_evaluator import record_result

router = APIRouter(prefix="/api/speech", tags=["speech"])


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

    # Step 2: Evaluate pronunciation via LLM
    evaluation = await evaluate_pronunciation(
        target_text=target_text,
        transcription=transcribed_text,
        confidence=confidence,
        level=level,
    )

    # Step 3: Record result
    is_correct = evaluation.get("is_correct", False)
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
        "evaluation": evaluation,
    }
