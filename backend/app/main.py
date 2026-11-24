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

    logger.info("Plan-Modell:  %s via %s", settings.llm_model, settings.llm_api_base_url)
    logger.info("Lokal-Modell: %s via %s", settings.ollama_model, settings.ollama_api_base_url)

    from .services import llm

    if not settings.llm_api_key:
        logger.warning("LLM_API_KEY not set. Training-plan generation will not work.")
    else:
        result = await llm.test_connection()
        if result["status"] == "ok":
            logger.info("Plan-LLM: Connected (%dms)", result["response_time_ms"])
        else:
            logger.warning("Plan-LLM: Connection failed: %s", result.get("error", "unknown"))

    local = await llm.test_connection(local=True)
    if local["status"] == "ok":
        logger.info("Ollama: Connected (%dms)", local["response_time_ms"])
    else:
        logger.warning("Ollama: Connection failed: %s", local.get("error", "unknown"))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend"}


@app.get("/v1/models")
async def list_models():
    # OpenCode probes port 8000 for a local vLLM server. This is not that server.
    return {"object": "list", "data": []}
