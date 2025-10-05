from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.models.forecast import ForecastRequest, ForecastResponse, HealthResponse, Location
from app.services.geocoding import Geocoder, GeocodingError
from app.services.nasa_power import NasaPowerClient

router = APIRouter()


def get_geocoder() -> Geocoder:
    return Geocoder()


def get_nasa_client() -> NasaPowerClient:
    return NasaPowerClient()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))


@router.post("/forecast", response_model=ForecastResponse)
async def forecast(
    payload: ForecastRequest,
    geocoder: Geocoder = Depends(get_geocoder),
    nasa_client: NasaPowerClient = Depends(get_nasa_client),
) -> ForecastResponse:
    if payload.location is None and not payload.query:
        raise HTTPException(status_code=400, detail="Either location coordinates or query must be provided")

    location: Location
    if payload.location:
        location = payload.location
    else:
        try:
            location = await geocoder.geocode(payload.query or "")
        except GeocodingError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return await nasa_client.precipitation_forecast(location, payload.event_date)
