"""Single entry point for SpecFuzzer LLM calls."""
from __future__ import annotations

from .config import settings
from .llm_remote import generate_remote


def generate_for_specfuzzer(
    user_prompt: str,
    *,
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """Route prompts to whichever provider is configured."""

    system_prompt = (
        "You are SpecFuzzer, an adversarial API test planner. "
        "You generate structured attack plans for HTTP APIs, "
        "with security edge cases and protocol violations."
    )

    provider = settings.llm_provider

    if provider == "remote":
        return generate_remote(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    raise ValueError(f"Unknown LLM_PROVIDER {provider!r}")
