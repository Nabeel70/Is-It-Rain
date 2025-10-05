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
from app.services.ensemble_forecaster import get_ensemble_forecaster, EnsembleForecaster
from app.services.ml_predictor import get_ml_predictor, MLPredictor

router = APIRouter()
settings = get_settings()


def get_geocoder() -> Geocoder:
    return Geocoder()


def get_nasa_client() -> NasaPowerClient:
    return NasaPowerClient()


def get_ensemble() -> EnsembleForecaster:
    return get_ensemble_forecaster()


def get_ml() -> MLPredictor:
    return get_ml_predictor()


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


@router.post("/forecast/ensemble", response_model=ForecastResponse)
async def ensemble_forecast(
    payload: ForecastRequest,
    geocoder: Geocoder = Depends(get_geocoder),
    ensemble: EnsembleForecaster = Depends(get_ensemble),
    db: ForecastDatabase | None = Depends(get_database),
) -> ForecastResponse:
    """
    Get ensemble forecast combining NASA POWER, ML model, and statistical analysis.
    
    This endpoint provides more accurate predictions by combining multiple methods:
    - NASA POWER satellite data (50% weight)
    - Machine learning model (30% weight)
    - Statistical trend analysis (20% weight)
    
    Expected accuracy: 70-80% for historical patterns
    """
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
    
    try:
        forecast_result = await ensemble.get_ensemble_forecast(location, payload.event_date)
        
        # Save to database if enabled
        if db:
            try:
                db.save_forecast(forecast_result)
                logger.info(
                    f"Saved ensemble forecast for {location.name} on {payload.event_date}"
                )
            except Exception as exc:
                logger.error(f"Failed to save forecast to database: {exc}")
        
        return forecast_result
        
    except Exception as exc:
        logger.error(f"Ensemble forecast failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate ensemble forecast"
        )


@router.get("/model/info")
async def get_model_info(
    ml: MLPredictor = Depends(get_ml),
) -> dict[str, Any]:
    """
    Get information about the ML model.
    
    Returns model metadata including:
    - Model availability status
    - Model type and architecture
    - Training metrics
    - Last updated date
    """
    return ml.get_model_info()


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
