import logging

import httpx

from ..config import settings
from ..prompts.evaluation import PRONUNCIATION_SYSTEM_PROMPT
from . import llm

logger = logging.getLogger(__name__)


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> dict:
    """Send audio to the Whisper service for transcription."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.whisper_url}/transcribe",
                files={"file": (filename, audio_bytes, "audio/webm")},
                data={"language": "fr"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("Whisper HTTP error: %s – %s", e.response.status_code, e.response.text[:300])
        return {"text": "", "segments": [], "language": "fr", "language_probability": 0.0, "error": str(e)}
    except httpx.RequestError as e:
        logger.error("Whisper connection error: %s", e)
        return {"text": "", "segments": [], "language": "fr", "language_probability": 0.0, "error": str(e)}


async def evaluate_pronunciation(
    target_text: str,
    transcription: str,
    confidence: float,
    level: str,
) -> dict:
    """Use LLM to evaluate pronunciation by comparing target vs transcription."""
    system_prompt = PRONUNCIATION_SYSTEM_PROMPT.format(
        level=level,
        target=target_text,
        transcription=transcription,
        confidence=confidence,
    )
    user_message = (
        f"Target: {target_text}\n"
        f"Student said: {transcription}\n"
        f"Confidence: {confidence}"
    )

    result = await llm.chat_json(system_prompt, user_message)
    return result
