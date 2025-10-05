from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    allowed_origins: List[str] = ["http://localhost:5173"]
    nasa_timeout: int = 15
    cache_ttl: int = 900
    http_proxy: str | None = None
    https_proxy: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""

    return Settings()
