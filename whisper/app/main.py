import os
import tempfile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from .model import get_model

app = FastAPI(title="Coach Français – Whisper STT")


@app.on_event("startup")
async def startup():
    get_model()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: str = Form(default=None),
):
    lang = language or os.getenv("WHISPER_LANGUAGE", "fr")

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=True) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

        model = get_model()
        segments_gen, info = model.transcribe(
            tmp.name,
            language=lang,
            beam_size=5,
            vad_filter=True,
        )

        segments = []
        full_text_parts = []
        for seg in segments_gen:
            segments.append(
                {
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip(),
                    "confidence": round(seg.avg_logprob, 4) if seg.avg_logprob else None,
                }
            )
            full_text_parts.append(seg.text.strip())

    return JSONResponse(
        {
            "text": " ".join(full_text_parts),
            "segments": segments,
            "language": info.language,
            "language_probability": round(info.language_probability, 4),
        }
    )
