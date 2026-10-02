"""Application configuration via pydantic-settings."""
from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    # Server
    app_env: str = "development"
    debug: bool = True
    # Comma-separated list — add your Vercel URL here after deploying frontend
    # e.g. "https://scamshield-ai.vercel.app,http://localhost:5173"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    # Database
    database_url: str = "sqlite+aiosqlite:///./scamshield.db"

    # ML
    model_dir: str = str(Path(__file__).parent.parent.parent / "ml" / "models")

    # Optional AI
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    # Upload
    max_upload_mb: int = 10

    # Rate limiting
    rate_limit_per_minute: int = 30

    @property
    def cors_origins(self) -> list[str]:
        origins = [o.strip() for o in self.allowed_origins.split(",") if o.strip()]
        # In production, always add a wildcard fallback so the API works
        # even before the exact Vercel URL is configured.
        # Once you set ALLOWED_ORIGINS to your real Vercel URL, remove "*".
        if self.app_env == "production" and "*" not in origins:
            origins.append("*")
        return origins

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def model_path(self) -> Path:
        return Path(self.model_dir)

    @property
    def ai_available(self) -> bool:
        return bool(self.gemini_api_key or self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
