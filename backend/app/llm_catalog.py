"""Curated OpenCode Console chat models for the coach.

IDs are the Console model IDs (no provider prefix) for the OpenAI-compatible
chat-completions base URL. Image, decision, and coding-only models are omitted.
`temperature` is False when the current catalog rejects that parameter.
"""

LLM_MODELS: list[dict] = [
    {
        "id": "claude-sonnet-5-5",
        "name": "Claude Sonnet 5.5",
        "tier": "standard",
        "temperature": False,
        "note": "Standard für Pläne, Dialoge und Übungen",
        "replaces": "claude-sonnet-4",
    },
    {
        "id": "claude-opus-5-5",
        "name": "Claude Opus 5.5",
        "tier": "flagship",
        "temperature": False,
        "note": "Stärkstes Sprach- und Planungsmodell",
        "replaces": "claude-opus-4-6",
    },
    {
        "id": "claude-haiku-5-5",
        "name": "Claude Haiku 5.5",
        "tier": "fast",
        "temperature": False,
        "note": "Kurzes Feedback, günstig",
        "replaces": "claude-haiku-4-5",
    },
    {
        "id": "gemini-4-argon",
        "name": "Gemini 4 Argon",
        "tier": "flagship",
        "temperature": False,
        "note": "Gemini-Flaggschiff",
        "replaces": "gemini-3-pro",
    },
    {
        "id": "gpt-6.2-sol",
        "name": "GPT 6.2 Sol",
        "tier": "standard",
        "temperature": True,
        "note": "Ausgewogenes GPT für Alltagssprache",
        "replaces": "gpt-5.2",
    },
    {
        "id": "gpt-6-luna",
        "name": "GPT 6 Luna",
        "tier": "fast",
        "temperature": True,
        "note": "Sehr günstiges GPT für kurze Antworten",
        "replaces": None,
    },
]

DEFAULT_LLM_MODEL = "claude-sonnet-5-5"
LLM_API_BASE_URL = "https://opencode.ai/inference/openai/v1"

_NO_TEMPERATURE = {m["id"] for m in LLM_MODELS if not m["temperature"]}


def supports_temperature(model: str) -> bool:
    return model not in _NO_TEMPERATURE
