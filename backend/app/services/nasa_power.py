from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

import httpx
from loguru import logger

from app.core.cache import cache_key, get_cache
from app.core.config import get_settings
from app.models.forecast import ForecastResponse, Location
from app.services.geocoding import reverse_geocode

NASA_DATASET = "NASA POWER (GPM IMERG derived)"


class NasaPowerClient:
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    def __init__(self) -> None:
        self._settings = get_settings()

    async def precipitation_forecast(self, location: Location, event_date: date) -> ForecastResponse:
        # Note: NASA POWER provides historical data, not forecasts
        # For future dates, we estimate based on historical averages
        cache = get_cache()
        # Use full precision coordinates for unique cache keys per location
        key = cache_key("nasa", str(location.latitude), str(location.longitude), event_date.isoformat())
        cached = cache.get(key)
        if cached:
            logger.info(f"Returning cached forecast for {location.name} on {event_date}")
            return cached
        
        logger.info(f"Fetching fresh NASA data for {location.latitude}, {location.longitude} on {event_date}")
        
        # Check if the date is in the future
        from datetime import datetime
        today = datetime.now().date()
        if event_date > today:
            logger.warning(f"Requested future date {event_date}, will use historical average")
            # For future dates, use the same day from previous year as a proxy
            proxy_date = event_date.replace(year=event_date.year - 1)
            return await self._fetch_historical_proxy(location, event_date, proxy_date)

        params = {
            "parameters": "PRECTOTCORR",
            "community": "RE",
            "longitude": location.longitude,
            "latitude": location.latitude,
            "start": event_date.strftime("%Y%m%d"),
            "end": event_date.strftime("%Y%m%d"),
            "format": "JSON",
        }
        proxies: dict[str, str] = {}
        if self._settings.http_proxy:
            proxies["http://"] = self._settings.http_proxy
        if self._settings.https_proxy:
            proxies["https://"] = self._settings.https_proxy
        client_kwargs: dict[str, Any] = {"timeout": self._settings.nasa_timeout}
        if proxies:
            client_kwargs["proxies"] = proxies

        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            payload: dict[str, Any] = response.json()

        try:
            daily_data = payload["properties"]["parameter"]["PRECTOTCORR"]
            raw_value = float(daily_data[event_date.strftime("%Y%m%d")])
            mm_value = max(raw_value, 0.0)
        except KeyError as exc:  # pragma: no cover - depends on upstream API
            logger.exception("NASA POWER response missing precipitation data", exc_info=exc)
            raise

        probability = self._precipitation_probability(mm_value)
        location_name = location.name or await reverse_geocode(location.latitude, location.longitude)

        forecast = ForecastResponse(
            location=Location(latitude=location.latitude, longitude=location.longitude, name=location_name),
            event_date=event_date,
            precipitation_probability=probability,
            precipitation_intensity_mm=mm_value,
            summary=self._summarize(probability, mm_value),
            nasa_dataset=NASA_DATASET,
            issued_at=datetime.now(timezone.utc),
        )
        cache[key] = forecast
        return forecast

    @staticmethod
    def _precipitation_probability(mm_value: float) -> float:
        if mm_value <= 0.2:
            return 0.1
        if mm_value <= 1:
            return 0.35
        if mm_value <= 5:
            return 0.6
        if mm_value <= 10:
            return 0.8
        return 0.95

    async def _fetch_historical_proxy(
        self, location: Location, event_date: date, proxy_date: date
    ) -> ForecastResponse:
        """Fetch historical data from a similar date as a proxy for future forecast."""
        params = {
            "parameters": "PRECTOTCORR",
            "community": "RE",
            "longitude": location.longitude,
            "latitude": location.latitude,
            "start": proxy_date.strftime("%Y%m%d"),
            "end": proxy_date.strftime("%Y%m%d"),
            "format": "JSON",
        }
        proxies: dict[str, str] = {}
        if self._settings.http_proxy:
            proxies["http://"] = self._settings.http_proxy
        if self._settings.https_proxy:
            proxies["https://"] = self._settings.https_proxy
        client_kwargs: dict[str, Any] = {"timeout": self._settings.nasa_timeout}
        if proxies:
            client_kwargs["proxies"] = proxies

        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            payload: dict[str, Any] = response.json()

        try:
            daily_data = payload["properties"]["parameter"]["PRECTOTCORR"]
            raw_value = float(daily_data[proxy_date.strftime("%Y%m%d")])
            mm_value = max(raw_value, 0.0)
        except KeyError as exc:
            logger.exception("NASA POWER response missing precipitation data", exc_info=exc)
            raise

        probability = self._precipitation_probability(mm_value)
        location_name = location.name or await reverse_geocode(location.latitude, location.longitude)

        forecast = ForecastResponse(
            location=Location(latitude=location.latitude, longitude=location.longitude, name=location_name),
            event_date=event_date,  # Use the original requested date
            precipitation_probability=probability,
            precipitation_intensity_mm=mm_value,
            summary=self._summarize(probability, mm_value) + f" (Based on {proxy_date.year} historical data)",
            nasa_dataset=NASA_DATASET + " (Historical Proxy)",
            issued_at=datetime.now(timezone.utc),
        )
        
        cache = get_cache()
        # Use full precision coordinates for cache key
        key = cache_key("nasa", str(location.latitude), str(location.longitude), event_date.isoformat())
        cache[key] = forecast
        logger.info(f"Cached forecast for {location.name} on {event_date} (using {proxy_date.year} historical data)")
        return forecast

    @staticmethod
    def _summarize(probability: float, mm_value: float) -> str:
        if probability < 0.2:
            return "Skies look clear. Enjoy your parade!"
        if probability < 0.5:
            return "Low chance of rain; keep an eye on the sky."
        if probability < 0.75:
            return "Moderate rain risk. Have a backup plan ready."
        if probability < 0.9:
            return "High chance of showers—pack ponchos and cover equipment."
        return "Severe rain threat expected. Consider rescheduling or moving indoors."
