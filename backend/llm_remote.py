"""Generic OpenAI compatible chat completions client."""
from __future__ import annotations

from typing import Any, Dict, List

import requests

from .config import settings


class LLMConfigError(RuntimeError):
    """Raised when remote LLM settings are missing."""


def _build_headers() -> Dict[str, str]:
    if not settings.llm_api_key:
        raise LLMConfigError("LLM_API_KEY not set in environment")
    return {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }


def _build_url(path: str) -> str:
    if not settings.llm_api_base:
        raise LLMConfigError("LLM_API_BASE not set in environment")

    base = settings.llm_api_base.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"


def generate_remote(
    system_prompt: str,
    user_prompt: str,
    *,
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """Call an OpenAI compatible /v1/chat/completions endpoint."""

    if not settings.llm_model:
        raise LLMConfigError("LLM_MODEL not set in environment")

    url = _build_url("v1/chat/completions")
    headers = _build_headers()

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    payload: Dict[str, Any] = {
        "model": settings.llm_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:  # pragma: no cover - defensive
        raise RuntimeError(f"Unexpected LLM response shape: {data}") from exc
