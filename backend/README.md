# Is It Rain API

This FastAPI application powers the "Will It Rain On My Parade?" experience by
combining NASA Earth observation data with open geospatial services to deliver
hyperlocal precipitation risk insights.

## Features

- Event-centric precipitation probability forecasts using the NASA POWER API
  (GPM IMERG-derived precipitation totals).
- Automatic geocoding of natural language locations using OpenStreetMap's
  Nominatim endpoint.
- Configurable caching layer to minimize upstream API calls.
- OpenAPI documentation served at `/docs` and `/redoc`.
- Ready for containerized deployment via Docker.

## Getting started

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

Create a `.env` file from `.env.example` and set the `ALLOWED_ORIGINS` for your
frontend as well as any proxy configuration.

## Testing

```bash
poetry run pytest
```

## Deployment

The application ships with production-ready defaults:

- Gunicorn/Uvicorn workers via `uvicorn[standard]`
- Graceful shutdown support and request logging
- Health check endpoint at `/health`

For container deployments use the provided Dockerfile at the repository root.
