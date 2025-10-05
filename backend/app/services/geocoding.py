from __future__ import annotations

from typing import Any

import httpx

from app.models.forecast import Location


class GeocodingError(RuntimeError):
    """Raised when a location cannot be resolved."""


class Geocoder:
    def __init__(self, user_agent: str = "is-it-rain-app") -> None:
        self._headers = {"User-Agent": user_agent}

    async def geocode(self, query: str) -> Location:
        async with httpx.AsyncClient(timeout=10, headers=self._headers) as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"format": "json", "limit": 1, "q": query},
            )
            response.raise_for_status()
            results: list[dict[str, Any]] = response.json()
            if not results:
                raise GeocodingError(f"Unable to geocode query: {query}")
            top = results[0]
            return Location(
                latitude=float(top["lat"]),
                longitude=float(top["lon"]),
                name=top.get("display_name"),
            )


async def reverse_geocode(latitude: float, longitude: float) -> str | None:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "format": "json",
                "lat": latitude,
                "lon": longitude,
                "zoom": 14,
            },
            headers={"User-Agent": "is-it-rain-app"},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data.get("display_name")
