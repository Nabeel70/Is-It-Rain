# Frontend build stage
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --legacy-peer-deps || npm install --legacy-peer-deps
COPY frontend ./
RUN npm run build

# Backend build stage
FROM python:3.11-slim AS backend-build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app/backend
COPY backend/pyproject.toml backend/README.md ./
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --only main
COPY backend ./

# Production image
FROM python:3.11-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=backend-build /app/backend /app
COPY --from=frontend-build /app/frontend/dist /app/static
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend preview image
FROM node:20-alpine AS frontend
WORKDIR /app
COPY --from=frontend-build /app/frontend/dist ./dist
RUN npm install -g serve
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173"]
