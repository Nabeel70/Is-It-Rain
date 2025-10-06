# Dockerfile Information

The `Dockerfile.local` file is for **local Docker development only**.

## Why is it renamed?

Railway auto-detects Dockerfiles and prioritizes them over other build configurations.
This caused Railway to deploy the frontend instead of the backend.

## How to use for local development

Rename it back temporarily:
```bash
mv Dockerfile.local Dockerfile
docker compose up --build
```

## For Railway Deployment

Railway uses the configuration from:
- `railway.json` (primary config)
- `nixpacks.toml` (build configuration)
- `Procfile` (start command)

These files ensure the backend is deployed correctly.
