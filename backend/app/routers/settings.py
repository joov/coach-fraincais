from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ..config import settings
from ..database import get_session
from ..llm_catalog import LLM_MODELS
from ..models import User
from ..services import llm

router = APIRouter(prefix="/api/settings", tags=["settings"])


class UserSettingsRequest(BaseModel):
    name: str | None = None
    current_level: str | None = None


class LLMSettingsRequest(BaseModel):
    llm_model: str | None = None
    model: str | None = None
    llm_temperature: float | None = None
    temperature: float | None = None
    llm_max_tokens: int | None = None
    max_tokens: int | None = None

    def resolved_model(self) -> str | None:
        return self.llm_model if self.llm_model is not None else self.model

    def resolved_temperature(self) -> float | None:
        return self.llm_temperature if self.llm_temperature is not None else self.temperature

    def resolved_max_tokens(self) -> int | None:
        return self.llm_max_tokens if self.llm_max_tokens is not None else self.max_tokens


@router.get("")
async def get_settings(session: Session = Depends(get_session)):
    user = session.exec(select(User)).first()
    return {
        "user": {
            "name": user.name if user else "",
            "current_level": user.current_level if user else "A1",
            "target_level": user.target_level if user else "A2",
        },
        "llm": {
            "api_base_url": settings.llm_api_base_url,
            "api_key_set": bool(settings.llm_api_key),
            "model": llm.get_model(),
            "temperature": llm.get_temperature(),
            "max_tokens": llm.get_max_tokens(),
        },
        "tts_speed": settings.tts_speed,
    }


@router.put("")
async def update_user_settings(
    req: UserSettingsRequest,
    session: Session = Depends(get_session),
):
    user = session.exec(select(User)).first()
    if not user:
        user = User(name=req.name or "Learner", current_level=req.current_level or "A1")
        session.add(user)
    else:
        if req.name is not None:
            user.name = req.name
        if req.current_level is not None:
            user.current_level = req.current_level
        session.add(user)

    session.commit()
    session.refresh(user)
    return {"status": "ok", "user": {"name": user.name, "current_level": user.current_level}}


@router.get("/llm/models")
async def list_llm_models():
    return {"models": LLM_MODELS}


@router.get("/llm")
async def get_llm_settings():
    return {
        "api_base_url": settings.llm_api_base_url,
        "api_key_set": bool(settings.llm_api_key),
        "model": llm.get_model(),
        "temperature": llm.get_temperature(),
        "max_tokens": llm.get_max_tokens(),
    }


@router.put("/llm")
async def update_llm_settings(req: LLMSettingsRequest):
    llm.update_runtime_settings(
        model=req.resolved_model(),
        temperature=req.resolved_temperature(),
        max_tokens=req.resolved_max_tokens(),
    )
    return {
        "status": "ok",
        "model": llm.get_model(),
        "temperature": llm.get_temperature(),
        "max_tokens": llm.get_max_tokens(),
    }


@router.post("/llm/test")
async def test_llm_connection():
    result = await llm.test_connection()
    return result
