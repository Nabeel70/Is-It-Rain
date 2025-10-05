from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.forecast import ForecastResponse, Location


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_forecast_requires_location(client):
    response = client.post("/api/forecast", json={"event_date": "2025-10-04"})
    assert response.status_code == 400


def test_forecast_success(monkeypatch, client):
    location = Location(latitude=40.0, longitude=-74.0, name="Mock City")

    monkeypatch.setattr("app.api.routes.Geocoder.geocode", AsyncMock(return_value=location))
    monkeypatch.setattr(
        "app.api.routes.NasaPowerClient.precipitation_forecast",
        AsyncMock(
            return_value=ForecastResponse(
                location=location,
                event_date=date(2025, 10, 4),
                precipitation_probability=0.8,
                precipitation_intensity_mm=4.2,
                summary="Mock summary",
                nasa_dataset="mock",
                issued_at=datetime.now(timezone.utc),
            )
        ),
    )

    response = client.post(
        "/api/forecast",
        json={"event_date": "2025-10-04", "query": "Mock City"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "Mock summary"
    assert body["location"]["name"] == "Mock City"
