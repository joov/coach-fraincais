import json
import logging

from openai import AsyncOpenAI

from ..config import settings
from ..llm_catalog import supports_temperature

logger = logging.getLogger(__name__)

_clients: dict[str, AsyncOpenAI] = {}

# Runtime overrides (set via settings API)
_runtime_model: str | None = None
_runtime_temperature: float | None = None
_runtime_max_tokens: int | None = None


def get_client(local: bool = False) -> AsyncOpenAI:
    key = "local" if local else "remote"
    if key not in _clients:
        if local:
            _clients[key] = AsyncOpenAI(
                base_url=settings.ollama_api_base_url,
                api_key=settings.ollama_api_key or "ollama",
            )
        else:
            _clients[key] = AsyncOpenAI(
                base_url=settings.llm_api_base_url,
                api_key=settings.llm_api_key,
            )
    return _clients[key]


def get_model(local: bool = False) -> str:
    if local:
        return settings.ollama_model
    return _runtime_model or settings.llm_model


def get_temperature() -> float:
    return _runtime_temperature if _runtime_temperature is not None else settings.llm_temperature


def get_max_tokens() -> int:
    return _runtime_max_tokens if _runtime_max_tokens is not None else settings.llm_max_tokens


async def _create_chat(client: AsyncOpenAI, kwargs: dict):
    """Call chat completions, dropping parameters the model rejects."""
    try:
        return await client.chat.completions.create(**kwargs)
    except Exception as exc:
        message = str(exc).lower()
        retry = dict(kwargs)
        changed = False
        if "temperature" in message and "temperature" in retry:
            retry.pop("temperature")
            changed = True
        if "response_format" in message or "json_object" in message:
            if "response_format" in retry:
                retry.pop("response_format")
                changed = True
        if not changed:
            raise
        logger.info("LLM retry without rejected parameters: %s", exc)
        return await client.chat.completions.create(**retry)


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
    local: bool = False,
    max_tokens: int | None = None,
) -> str:
    """Send a chat completion. local=True uses Ollama, otherwise the plan model."""
    client = get_client(local)
    model = get_model(local)

    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": max_tokens if max_tokens is not None else get_max_tokens(),
    }
    if supports_temperature(model):
        kwargs["temperature"] = get_temperature()

    if response_format == "json":
        kwargs["response_format"] = {"type": "json_object"}

    logger.info("LLM request: local=%s model=%s", local, model)
    response = await _create_chat(client, kwargs)
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


async def chat_json(
    system_prompt: str,
    user_message: str,
    local: bool = False,
    max_tokens: int | None = None,
) -> dict:
    """Send a chat completion request and parse the JSON response."""
    raw = await chat(
        system_prompt,
        user_message,
        response_format="json",
        local=local,
        max_tokens=max_tokens,
    )
    cleaned = _extract_json(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM JSON response: %s", cleaned[:500])
        return {}


async def test_connection(local: bool = False) -> dict:
    """Test the plan model, or the local Ollama model when local=True."""
    import time

    client = get_client(local)
    model = get_model(local)
    start = time.time()
    try:
        test_kwargs: dict = {
            "model": model,
            "messages": [{"role": "user", "content": "Dis 'bonjour' en un mot."}],
            "max_tokens": 10,
        }
        if supports_temperature(model):
            test_kwargs["temperature"] = 0
        response = await _create_chat(client, test_kwargs)
        elapsed = int((time.time() - start) * 1000)
        return {
            "status": "ok",
            "model": model,
            "response_time_ms": elapsed,
            "message": response.choices[0].message.content or "",
        }
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        return {
            "status": "error",
            "model": model,
            "response_time_ms": elapsed,
            "error": str(e),
        }
