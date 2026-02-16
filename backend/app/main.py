import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import create_db_and_tables
from .routers import plan, lessons, exercises, speech, progress, settings as settings_router

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger(__name__)

app = FastAPI(title="Coach Français", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan.router)
app.include_router(lessons.router)
app.include_router(exercises.router)
app.include_router(speech.router)
app.include_router(progress.router)
app.include_router(settings_router.router)


@app.on_event("startup")
async def startup():
    logger.info("Creating database tables...")
    create_db_and_tables()

    logger.info("LLM-Provider: %s", settings.llm_api_base_url)
    logger.info("LLM-Modell:   %s", settings.llm_model)

    if not settings.llm_api_key:
        logger.warning("LLM_API_KEY not set. Plan generation and exercise creation will not work.")
    else:
        from .services import llm

        result = await llm.test_connection()
        if result["status"] == "ok":
            logger.info("LLM-Status: Connected (%dms)", result["response_time_ms"])
        else:
            logger.warning("LLM-Status: Connection failed: %s", result.get("error", "unknown"))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend"}
