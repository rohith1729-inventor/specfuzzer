"""Runtime configuration for backend components."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment driven config for LLM gateway and backend."""

    llm_provider: str = "remote"
    llm_api_base: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    target_base_url: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
