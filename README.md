# Will It Rain On My Parade?

End-to-end solution for the NASA Space Apps Challenge 2025 that forecasts
precipitation risk for outdoor events using NASA's POWER (GPM IMERG-derived)
precipitation data combined with open geocoding services.

**Live Demo**: *Deploy using instructions in [DEPLOYMENT.md](docs/DEPLOYMENT.md)*

**Built for**: [NASA Space Apps Challenge 2025 - "Will It Rain On My Parade?"](https://www.spaceappschallenge.org/2025/challenges/will-it-rain-on-my-parade/)

---

## Features

✨ **Key Capabilities**:
- 🌧️ **Precipitation Forecasting**: Get rain probability and intensity for any date and location
- 🗺️ **Smart Geocoding**: Enter location names or coordinates
- 📊 **Data Visualization**: Interactive maps and charts showing precipitation data
- ⚡ **Fast & Cached**: 15-minute response caching for optimal performance
- 🌍 **Global Coverage**: Works anywhere in the world (NASA POWER dataset)
- 🔒 **Production Ready**: Docker deployment, CORS configuration, health checks
- 📱 **Responsive UI**: Beautiful, mobile-friendly interface built with React + Tailwind

**Data Sources**:
- **NASA POWER API**: GPM IMERG precipitation data (free, no authentication)
- **OpenStreetMap Nominatim**: Geocoding and reverse geocoding
- **Daily Updates**: Near real-time precipitation data

## Table of contents

- [Features](#features)
- [Architecture](#architecture)
- [Datasets](#datasets)
- [Quick Start](#quick-start)
- [Local development](#local-development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Operational playbook](#operational-playbook)
- [Step-by-step build guide](#step-by-step-build-guide)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The system is composed of:

- **Frontend** (`frontend/`): React + Vite single-page app with Tailwind, Leaflet
  maps, and Recharts visualizations.
- **Backend** (`backend/`): FastAPI service that geocodes user locations,
  retrieves NASA precipitation data, applies heuristic risk scoring, and
  responds with a structured forecast.
- **Infrastructure** (`infra/`): Docker-based setup for local orchestration and
  deployment artifacts.
- **Docs & Data** (`docs/`, `data/`): Architectural overview and dataset usage
  guidelines.

A visual diagram is provided in `docs/architecture.md`.

## Quick Start

Get the application running in under 5 minutes! For detailed instructions, see [QUICKSTART.md](docs/QUICKSTART.md).

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Nabeel70/Is-It-Rain.git
cd Is-It-Rain

# Start with Docker Compose
cd infra
docker compose up --build
```

Access the app at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

**Backend**:
```bash
cd backend
pip install poetry
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Need help?** See the [Quick Start Guide](docs/QUICKSTART.md) for troubleshooting and detailed instructions.

## Datasets

- **NASA POWER API** (`PRECTOTCORR`): Daily corrected precipitation totals
  derived from the GPM IMERG constellation. Free, no authentication required.
- **OpenStreetMap Nominatim**: Geocoding and reverse geocoding to convert human
  place names into coordinates and friendly labels.

See `data/README.md` for sample queries and expansion ideas (e.g., MERRA-2,
IMERG half-hourly data via GES DISC).

## Local development

1. **Backend**
   ```bash
   cd backend
   poetry install
   cp .env.example .env
   poetry run uvicorn app.main:app --reload
   ```
2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Visit http://localhost:5173. The Vite dev server proxies `/api` to the
   FastAPI backend at http://localhost:8000.

Alternatively, run the full stack with Docker:

```bash
cd infra
docker compose up --build
```

## Testing

- **Backend**: `cd backend && poetry run pytest`
- **Frontend**: `cd frontend && npm run lint`

## Deployment

- Build the production backend image: `docker build --target backend -t is-it-rain-api .`
- Deploy behind a reverse proxy (e.g., Azure App Service, AWS ECS, or Google
  Cloud Run). Static frontend assets (Vite build output) are copied into the
  backend image under `/app/static` and can be served via a CDN or the API
  container.

## Operational playbook

- Rate limiting: configure an API gateway (e.g., Cloudflare) to shield external
  access to NASA POWER and OpenStreetMap.
- Caching: the backend uses an in-memory TTL cache by default; swap in Redis by
  replacing `app/core/cache.py` with a Redis client if horizontal scaling is
  required.
- Observability: integrate FastAPI logging with OpenTelemetry exporters for
  traces/metrics.

## Step-by-step build guide

1. Clone the repository and review the architecture overview in
   `docs/architecture.md`.
2. Set up Python 3.11 and Node 20 runtimes (or use Docker).
3. Install backend dependencies with Poetry, configure environment variables via
   `.env`, and run the FastAPI dev server.
4. Install frontend dependencies with npm, start the Vite dev server, and verify
   that event submissions return forecasts.
5. Explore dataset expansion opportunities by inspecting `data/README.md` and
   referencing NASA POWER documentation. Consider augmenting with IMERG
   half-hourly or ECMWF reanalysis for ensemble modeling.
6. Harden for production by enabling HTTPS, setting `ALLOWED_ORIGINS` to your
   domain, and deploying the Docker image to your chosen platform.
7. Monitor NASA and OpenStreetMap API quotas, add retries/backoff if your event
   load increases, and document operations in `docs/`.

## Documentation

Comprehensive documentation is available:

- 📚 **[API.md](docs/API.md)**: Complete REST API documentation
  - All endpoints with request/response schemas
  - Code examples in TypeScript and Python
  - Error handling and best practices
  
- 🚀 **[DEPLOYMENT.md](docs/DEPLOYMENT.md)**: Production deployment guide
  - Docker, AWS, Azure, GCP, Kubernetes options
  - Security configuration
  - Monitoring and troubleshooting
  - Cost optimization
  
- 📊 **[DATASETS.md](docs/DATASETS.md)**: Dataset documentation
  - NASA POWER API details
  - GPM IMERG precipitation data
  - OpenStreetMap geocoding
  - Data quality and limitations
  
- 🏗️ **[architecture.md](docs/architecture.md)**: System architecture overview
- 🔧 **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**: Comprehensive troubleshooting guide
- 🚀 **[QUICKSTART.md](docs/QUICKSTART.md)**: Quick start guide for beginners

## Contributing

Contributions are welcome! This project was built for the NASA Space Apps Challenge 2025.

**How to contribute**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Guidelines**:
- Follow existing code style
- Add tests for new features
- Update documentation
- Run tests before submitting: `poetry run pytest` (backend), `npm run lint` (frontend)

## License

This project is developed for educational purposes as part of the NASA Space Apps Challenge 2025.

**Data Attribution**:
- NASA POWER API (GPM IMERG) - Public domain
- OpenStreetMap data - © OpenStreetMap contributors (ODbL)

## Acknowledgments

- **NASA** for providing the POWER API and GPM IMERG dataset
- **OpenStreetMap** contributors for geocoding services
- **NASA Space Apps Challenge** for the inspiration and challenge framework

---

**Questions or Issues?** Open an issue on [GitHub](https://github.com/Nabeel70/Is-It-Rain/issues)

**Built with** ❤️ **for the NASA Space Apps Challenge 2025**
