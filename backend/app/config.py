from pydantic_settings import BaseSettings

from .llm_catalog import DEFAULT_LLM_MODEL, LLM_API_BASE_URL


class Settings(BaseSettings):
    # LLM
    llm_api_base_url: str = LLM_API_BASE_URL
    llm_api_key: str = ""
    llm_model: str = DEFAULT_LLM_MODEL
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # Local Ollama: lessons, exercises, feedback. Not the training plan.
    ollama_api_base_url: str = "http://host.docker.internal:11434/v1"
    ollama_api_key: str = "ollama"
    ollama_model: str = "gemma4"

    # Whisper
    whisper_url: str = "http://whisper:9000"

    # DB
    database_url: str = "sqlite:///data/coach.db"

    # General
    tts_speed: float = 0.85
    log_level: str = "info"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
