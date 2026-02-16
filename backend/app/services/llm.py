import json
import logging

from openai import AsyncOpenAI

from ..config import settings

logger = logging.getLogger(__name__)

_client: AsyncOpenAI | None = None

# Runtime overrides (set via settings API)
_runtime_model: str | None = None
_runtime_temperature: float | None = None
_runtime_max_tokens: int | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            base_url=settings.llm_api_base_url,
            api_key=settings.llm_api_key,
        )
    return _client


def get_model() -> str:
    return _runtime_model or settings.llm_model


def get_temperature() -> float:
    return _runtime_temperature if _runtime_temperature is not None else settings.llm_temperature


def get_max_tokens() -> int:
    return _runtime_max_tokens if _runtime_max_tokens is not None else settings.llm_max_tokens


def update_runtime_settings(
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
):
    global _runtime_model, _runtime_temperature, _runtime_max_tokens
    if model is not None:
        _runtime_model = model
    if temperature is not None:
        _runtime_temperature = temperature
    if max_tokens is not None:
        _runtime_max_tokens = max_tokens


async def chat(
    system_prompt: str,
    user_message: str,
    response_format: str = "text",
) -> str:
    """Send a chat completion request to the LLM."""
    client = get_client()

    kwargs: dict = {
        "model": get_model(),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": get_temperature(),
        "max_tokens": get_max_tokens(),
    }

    if response_format == "json":
        kwargs["response_format"] = {"type": "json_object"}

    logger.info("LLM request: model=%s", get_model())
    response = await client.chat.completions.create(**kwargs)
    content = response.choices[0].message.content or ""
    logger.info("LLM response: %d chars", len(content))
    return content


def _extract_json(raw: str) -> str:
    """Extract JSON from a response that may be wrapped in markdown code fences."""
    stripped = raw.strip()
    # Remove ```json ... ``` wrapping
    if stripped.startswith("```"):
        # Find the end of the first line (```json or ```)
        first_newline = stripped.index("\n") if "\n" in stripped else len(stripped)
        stripped = stripped[first_newline + 1:]
        # Remove trailing ```
        if stripped.rstrip().endswith("```"):
            stripped = stripped.rstrip()[:-3].rstrip()
    return stripped


async def chat_json(system_prompt: str, user_message: str) -> dict:
    """Send a chat completion request and parse the JSON response."""
    raw = await chat(system_prompt, user_message, response_format="json")
    cleaned = _extract_json(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM JSON response: %s", cleaned[:500])
        return {}


async def test_connection() -> dict:
    """Test the LLM connection and return status."""
    import time

    client = get_client()
    start = time.time()
    try:
        response = await client.chat.completions.create(
            model=get_model(),
            messages=[{"role": "user", "content": "Dis 'bonjour' en un mot."}],
            max_tokens=10,
        )
        elapsed = int((time.time() - start) * 1000)
        return {
            "status": "ok",
            "model": get_model(),
            "response_time_ms": elapsed,
            "message": response.choices[0].message.content or "",
        }
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        return {
            "status": "error",
            "model": get_model(),
            "response_time_ms": elapsed,
            "error": str(e),
        }
