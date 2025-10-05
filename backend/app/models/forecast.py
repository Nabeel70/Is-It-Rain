from datetime import date, datetime

from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    name: str | None = None


class ForecastRequest(BaseModel):
    event_date: date
    location: Location | None = None
    query: str | None = Field(
        default=None,
        description="Free-form location string to be geocoded if latitude/longitude are not provided.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_date": "2025-10-05",
                    "query": "Central Park, New York, NY",
                }
            ]
        }
    }


class ForecastResponse(BaseModel):
    location: Location
    event_date: date
    precipitation_probability: float = Field(..., ge=0, le=1)
    precipitation_intensity_mm: float = Field(..., ge=0)
    summary: str
    nasa_dataset: str
    issued_at: datetime


class HealthResponse(BaseModel):
    status: str = "ok"
    timestamp: datetime
