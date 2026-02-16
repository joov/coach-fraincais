from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    llm_api_base_url: str = "https://openrouter.ai/api/v1"
    llm_api_key: str = ""
    llm_model: str = "anthropic/claude-sonnet-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # Whisper
    whisper_url: str = "http://whisper:9000"

    # DB
    database_url: str = "sqlite:///data/coach.db"

    # General
    tts_speed: float = 0.85
    log_level: str = "info"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
