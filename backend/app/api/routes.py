from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.core.config import get_settings
from app.core.database import ForecastDatabase
from app.models.forecast import ForecastRequest, ForecastResponse, HealthResponse, Location
from app.services.geocoding import Geocoder, GeocodingError
from app.services.nasa_power import NasaPowerClient

router = APIRouter()
settings = get_settings()


def get_geocoder() -> Geocoder:
    return Geocoder()


def get_nasa_client() -> NasaPowerClient:
    return NasaPowerClient()


def get_database() -> ForecastDatabase | None:
    if settings.database_enabled:
        return ForecastDatabase(settings.database_path)
    return None


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))


@router.post("/forecast", response_model=ForecastResponse)
async def forecast(
    payload: ForecastRequest,
    geocoder: Geocoder = Depends(get_geocoder),
    nasa_client: NasaPowerClient = Depends(get_nasa_client),
    db: ForecastDatabase | None = Depends(get_database),
) -> ForecastResponse:
    if payload.location is None and not payload.query:
        raise HTTPException(
            status_code=400, 
            detail="Either location coordinates or query must be provided"
        )

    location: Location
    if payload.location:
        location = payload.location
    else:
        try:
            location = await geocoder.geocode(payload.query or "")
        except GeocodingError as exc:
            logger.error(f"Geocoding failed for query '{payload.query}': {exc}")
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    forecast_result = await nasa_client.precipitation_forecast(location, payload.event_date)
    
    # Save to database if enabled
    if db:
        try:
            db.save_forecast(forecast_result)
            logger.info(
                f"Saved forecast for {location.name} on {payload.event_date}"
            )
        except Exception as exc:
            logger.error(f"Failed to save forecast to database: {exc}")
    
    return forecast_result


@router.get("/stats")
async def get_stats(
    db: ForecastDatabase | None = Depends(get_database),
) -> dict[str, Any]:
    """Get database statistics."""
    if not db:
        raise HTTPException(status_code=503, detail="Database not enabled")
    
    try:
        return db.get_statistics()
    except Exception as exc:
        logger.error(f"Failed to get statistics: {exc}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


@router.get("/history")
async def get_history(
    latitude: float,
    longitude: float,
    limit: int = 10,
    db: ForecastDatabase | None = Depends(get_database),
) -> list[dict[str, Any]]:
    """Get forecast history for a location."""
    if not db:
        raise HTTPException(status_code=503, detail="Database not enabled")
    
    try:
        return db.get_forecast_history(latitude, longitude, limit)
    except Exception as exc:
        logger.error(f"Failed to get forecast history: {exc}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")
