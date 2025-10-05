from datetime import date
from unittest.mock import AsyncMock, patch

import pytest

from app.models.forecast import Location
from app.services.nasa_power import NasaPowerClient


@pytest.mark.asyncio
async def test_precipitation_probability_conversion(monkeypatch):
    client = NasaPowerClient()
    location = Location(latitude=40.7128, longitude=-74.0060)
    event_date = date(2025, 10, 4)

    async def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "properties": {
                        "parameter": {
                            "PRECTOTCORR": {event_date.strftime("%Y%m%d"): 6.0}
                        }
                    }
                }

        return MockResponse()

    with patch("httpx.AsyncClient.get", new=mock_get):
        with patch("app.services.nasa_power.reverse_geocode", new=AsyncMock(return_value="NYC")):
            forecast = await client.precipitation_forecast(location, event_date)

    assert forecast.precipitation_probability == pytest.approx(0.8)
    assert forecast.summary.startswith("High chance")
    assert forecast.location.name == "NYC"
