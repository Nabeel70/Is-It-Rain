# Infrastructure

- `docker-compose.yml` runs the FastAPI backend and the static frontend preview
  (`serve`) in tandem for demos.
- The root `Dockerfile` supports multi-stage builds for production (backend) and
  preview (frontend) targets.

## Local stack

```bash
cd infra
docker compose up --build
```

The frontend will be available at http://localhost:5173 and proxies API calls to
http://localhost:8000.
