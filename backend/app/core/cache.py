from cachetools import TTLCache

from .config import get_settings


_settings = get_settings()
_cache = TTLCache(maxsize=256, ttl=_settings.cache_ttl)


def cache_key(*parts: str) -> str:
    """Generate a deterministic cache key from string parts.
    
    Note: Converts all parts to strings to handle numeric types.
    """
    return ":".join(str(p) for p in parts)


def get_cache() -> TTLCache:
    return _cache
