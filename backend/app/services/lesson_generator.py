import logging

from sqlmodel import Session

from ..models import Lesson
from ..prompts.lesson import LESSON_SYSTEM_PROMPT
from ..prompts.exercise import EXERCISE_SYSTEM_PROMPT
from . import llm

logger = logging.getLogger(__name__)


async def generate_lesson_content(session: Session, lesson: Lesson, level: str) -> Lesson:
    """Generate dialogues and grammar box for a lesson using the LLM."""

    if lesson.dialogues and lesson.dialogues.get("informal"):
        logger.info("Lesson %d already has content, skipping generation", lesson.number)
        return lesson

    system_prompt = LESSON_SYSTEM_PROMPT.format(level=level)
    user_message = (
        f"Create content for Lesson {lesson.number}: '{lesson.title}'\n"
        f"Topic: {lesson.topic}\n"
        f"Grammar focus: {lesson.grammar_focus}\n"
        f"Student level: {level}"
    )

    content = await llm.chat_json(system_prompt, user_message)

    lesson.dialogues = content.get("dialogues", {})
    lesson.grammar_box = content.get("grammar_box", {})

    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    return lesson


async def generate_exercises(session: Session, lesson: Lesson, level: str) -> Lesson:
    """Generate exercises for a lesson using the LLM."""

    if lesson.exercises:
        logger.info("Lesson %d already has exercises, skipping generation", lesson.number)
        return lesson

    system_prompt = EXERCISE_SYSTEM_PROMPT.format(
        level=level,
        topic=lesson.topic,
        grammar_focus=lesson.grammar_focus,
    )
    user_message = (
        f"Create exercises for Lesson {lesson.number}: '{lesson.title}'\n"
        f"Topic: {lesson.topic}\n"
        f"Grammar focus: {lesson.grammar_focus}"
    )

    content = await llm.chat_json(system_prompt, user_message)

    lesson.exercises = content.get("exercises", [])

    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    return lesson
