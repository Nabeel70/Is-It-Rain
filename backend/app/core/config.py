from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # CORS settings
    allowed_origins: str | List[str] = "http://localhost:5173,http://localhost:8000"
    
    # NASA API settings
    nasa_timeout: int = 15
    
    # Cache settings
    cache_ttl: int = 900  # 15 minutes
    
    # Proxy settings
    http_proxy: str | None = None
    https_proxy: str | None = None
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # Database
    database_enabled: bool = True
    database_path: str = "data/forecasts.db"
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_allowed_origins(cls, v: str | List[str]) -> List[str]:
        """Split comma-separated string into list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""

    return Settings()
