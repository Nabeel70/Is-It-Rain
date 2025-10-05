"""Database module for storing forecast history and analytics."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models.forecast import ForecastResponse


class ForecastDatabase:
    """SQLite database for storing forecast history."""

    def __init__(self, db_path: str = "data/forecasts.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    location_name TEXT,
                    event_date TEXT NOT NULL,
                    precipitation_probability REAL NOT NULL,
                    precipitation_intensity_mm REAL NOT NULL,
                    summary TEXT NOT NULL,
                    nasa_dataset TEXT NOT NULL,
                    issued_at TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_event_date 
                ON forecasts(event_date)
            """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_location 
                ON forecasts(latitude, longitude)
            """
            )
            conn.commit()

    def save_forecast(self, forecast: ForecastResponse) -> int:
        """Save a forecast to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO forecasts (
                    latitude, longitude, location_name, event_date,
                    precipitation_probability, precipitation_intensity_mm,
                    summary, nasa_dataset, issued_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    forecast.location.latitude,
                    forecast.location.longitude,
                    forecast.location.name,
                    forecast.event_date.isoformat(),
                    forecast.precipitation_probability,
                    forecast.precipitation_intensity_mm,
                    forecast.summary,
                    forecast.nasa_dataset,
                    forecast.issued_at.isoformat(),
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def get_forecast_history(
        self, latitude: float, longitude: float, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Get forecast history for a location."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM forecasts 
                WHERE latitude = ? AND longitude = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (latitude, longitude, limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self) -> dict[str, Any]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT 
                    COUNT(*) as total_forecasts,
                    AVG(precipitation_probability) as avg_rain_probability,
                    AVG(precipitation_intensity_mm) as avg_precipitation_mm,
                    COUNT(DISTINCT latitude || ',' || longitude) as unique_locations
                FROM forecasts
            """
            )
            row = cursor.fetchone()
            return {
                "total_forecasts": row[0],
                "avg_rain_probability": round(row[1] or 0, 3),
                "avg_precipitation_mm": round(row[2] or 0, 2),
                "unique_locations": row[3],
            }
