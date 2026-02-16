from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..services.progress_tracker import get_progress_summary, get_error_analysis

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("")
async def get_progress(session: Session = Depends(get_session)):
    user = session.exec(select(User)).first()
    if not user:
        return {"progress": None}

    summary = get_progress_summary(session, user.id)
    return {"user": user.name, "level": user.current_level, **summary}


@router.get("/level")
async def get_level_assessment(session: Session = Depends(get_session)):
    user = session.exec(select(User)).first()
    if not user:
        return {"assessment": None}

    analysis = await get_error_analysis(session, user.id, user.current_level)
    return analysis
