# Will It Rain On My Parade? 🌧️☔

![NASA Space Apps Challenge 2025](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge%202025-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal)
![React](https://img.shields.io/badge/React-18.3+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Production-ready application for predicting rain probability using NASA Earth observation data**

End-to-end solution for the NASA Space Apps Challenge 2025 that provides precipitation forecasts for outdoor events using NASA's POWER API (GPM IMERG-derived precipitation data) combined with OpenStreetMap geocoding services.

## 🎯 Features

- **🛰️ Real NASA Data**: Leverages GPM IMERG satellite precipitation measurements via NASA POWER API
- **📍 Global Coverage**: Works for any location worldwide using OpenStreetMap Nominatim
- **📊 Smart Forecasting**: Historical data analysis with proxy estimates for future dates
- **⚡ Fast & Cached**: 15-minute response caching for optimal performance
- **🗺️ Interactive Maps**: Visual location confirmation with Leaflet
- **📈 Analytics**: Built-in statistics and forecast history tracking
- **🔒 Production-Ready**: Rate limiting, error handling, logging, and database storage
- **🐳 Docker Support**: One-command deployment with Docker Compose
- **📱 Responsive UI**: Modern, mobile-friendly interface built with React and Tailwind CSS

## 🏗️ Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Datasets](#datasets)
- [Local Development](#local-development)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Nabeel70/Is-It-Rain.git
cd Is-It-Rain

# Start with Docker Compose
cd infra
docker compose up --build
```

Access the application:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Setup

**Backend**:
```bash
cd backend
pip install poetry
poetry install
poetry run uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

## 🏗️ Architecture

The system is composed of:

- **Frontend** (`frontend/`): 
  - React 18 + Vite for blazing-fast development
  - Tailwind CSS for modern, responsive styling
  - Leaflet for interactive maps
  - Recharts for data visualization
  - TanStack Query for efficient API state management

- **Backend** (`backend/`): 
  - FastAPI for high-performance async API
  - Poetry for dependency management
  - SQLite database for forecast history
  - In-memory caching with TTL
  - Rate limiting middleware
  - Structured logging with Loguru

- **Infrastructure** (`infra/`): 
  - Multi-stage Dockerfile for optimized builds
  - Docker Compose for local development
  - Production-ready configuration

- **Data & Docs** (`docs/`, `data/`): 
  - Comprehensive API documentation
  - Deployment guides
  - Architecture diagrams
  - Dataset information

**System Flow**:
```
User Input → Frontend → Backend API → [Geocoding] → NASA POWER API → 
[Data Processing] → [Risk Calculation] → [Database Storage] → Response → UI Display
```

A visual diagram is provided in `docs/architecture.md`.

## 📊 Datasets

### NASA POWER API

**Primary Data Source**: NASA's POWER (Prediction Of Worldwide Energy Resources) project

- **Parameter**: `PRECTOTCORR` - Corrected Total Precipitation
- **Source**: GPM IMERG (Global Precipitation Measurement - Integrated Multi-satellitE Retrievals for GPM)
- **Coverage**: Global, land and ocean
- **Resolution**: Daily precipitation totals in millimeters
- **Temporal Range**: Historical data from 2000 to ~3 days ago
- **Access**: Free, no authentication required
- **API**: https://power.larc.nasa.gov/api/temporal/daily/point

**Important**: NASA POWER provides historical observations, not future forecasts. For future dates, our application uses historical data from the same date in the previous year as a proxy estimate.

**Data Quality**:
- ✅ Satellite-derived measurements
- ✅ Corrected for systematic biases
- ✅ Quality-controlled by NASA
- ✅ Updated daily

### OpenStreetMap Nominatim

**Geocoding Service**: Converts place names to coordinates

- **Coverage**: Global
- **Accuracy**: Street-level precision for most locations
- **Rate Limit**: 1 request/second (we respect this limit)
- **Cost**: Free
- **Attribution**: Required (included in our footer)

### Future Enhancements

Potential additional data sources (see `data/README.md`):

- **MERRA-2**: Atmospheric reanalysis for enhanced predictions
- **IMERG Half-Hourly**: Higher temporal resolution data
- **MODIS**: Cloud cover and atmospheric moisture
- **Weather Forecast APIs**: For true future forecasts (OpenWeatherMap, NOAA)

## 📡 How It Works

### ⚠️ Important: This App Uses Historical Satellite Data, Not Forecasts

**NASA POWER provides historical observations from satellites, not predictive forecasts.**

### For Historical Dates (Past 3+ Days)

1. User enters event date and location
2. Location is geocoded to coordinates (lat/lon)
3. **NASA POWER API returns ACTUAL measured precipitation** from GPM IMERG satellites
4. Probability is calculated based on measured precipitation amounts
5. Results show **what actually happened** on that date
6. Data is cached (15 min) and stored in database

**Example**: Query "London, Oct 3, 2024" → Returns actual satellite measurement: 0.0mm → "Clear skies"

### For Future Dates (Proxy Estimate)

Since NASA only has historical data, for future dates:

1. User enters future event date and location
2. System automatically uses **same date from previous year**
3. Historical data is retrieved (e.g., Dec 25, 2025 uses Dec 25, 2024 data)
4. Response clearly labeled: "(Based on 2024 historical data)"
5. This provides seasonal pattern estimate, not actual forecast

**Example**: Query "Paris, Dec 25, 2025" → Uses Dec 25, 2024 data → 0.57mm → "35% chance"

### 🎯 What This Means For You

**✅ Accurate For**:
- Understanding seasonal rainfall patterns
- Planning events based on historical weather
- Comparing precipitation across locations
- Viewing real satellite measurements

**❌ NOT Accurate For**:
- Actual weather forecasting
- Real-time current conditions (3-7 day lag)
- Predicting specific future weather
- 99% accuracy claims

### Probability Calculation

Rain probability is estimated using precipitation thresholds:

| Precipitation (mm) | Probability | Summary |
|-------------------|-------------|----------|
| ≤ 0.2 | 10% | Skies look clear |
| 0.2 - 1.0 | 35% | Low chance of rain |
| 1.0 - 5.0 | 60% | Moderate rain risk |
| 5.0 - 10.0 | 80% | High chance of showers |
| > 10.0 | 95% | Severe rain threat |

## 💻 Local Development

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 20 or higher  
- **Poetry**: Python package manager
- **Docker** (optional): For containerized development

### Backend Setup

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install poetry
   poetry install
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for local development)
   ```

3. **Run Development Server**:
   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Verify**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run Development Server**:
   ```bash
   npm run dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:5173
   - The Vite dev server automatically proxies `/api` requests to the backend

### Docker Development

Run the full stack with one command:

```bash
cd infra
docker compose up --build
```

**Services**:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

**Useful Commands**:
```bash
# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild specific service
docker compose up --build api

# Run in background
docker compose up -d
```

## 📚 API Documentation

### Quick Example

```bash
# Get forecast for New York on Christmas 2025
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "event_date": "2025-12-25",
    "query": "Central Park, New York"
  }'
```

**Response**:
```json
{
  "location": {
    "latitude": 40.785091,
    "longitude": -73.968285,
    "name": "Central Park, Manhattan, ..."
  },
  "event_date": "2025-12-25",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 2.5,
  "summary": "Low chance of rain; keep an eye on the sky.",
  "nasa_dataset": "NASA POWER (GPM IMERG derived)",
  "issued_at": "2025-10-05T10:42:15.123456Z"
}
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/forecast` | Get precipitation forecast |
| `GET` | `/api/stats` | Get system statistics |
| `GET` | `/api/history` | Get forecast history for location |

**Full API Documentation**: See `docs/API.md` or visit `/docs` when running

### Rate Limits

- **Per Minute**: 60 requests (configurable)
- **Per Hour**: 1000 requests (configurable)

Rate limit headers included in every response:
- `X-RateLimit-Minute-Remaining`
- `X-RateLimit-Hour-Remaining`

## 🧪 Testing

### Backend Tests

```bash
cd backend
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_nasa_power.py

# Verbose output
poetry run pytest -v
```

**Test Coverage**:
- Unit tests for NASA POWER client
- Integration tests for API endpoints
- Geocoding service tests
- Database operations tests

### Frontend Tests

```bash
cd frontend

# Lint check
npm run lint

# Type check
npm run type-check

# Build test
npm run build
```

### Manual Testing

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Forecast Endpoint**:
   ```bash
   curl -X POST http://localhost:8000/api/forecast \
     -H "Content-Type: application/json" \
     -d '{"event_date": "2025-10-10", "query": "Paris, France"}'
   ```

3. **Test Rate Limiting**:
   ```bash
   for i in {1..70}; do
     curl http://localhost:8000/api/health
   done
   # Should see 429 error after 60 requests
   ```

4. **Frontend UI Testing**:
   - Navigate to http://localhost:5173
   - Enter various locations and dates
   - Verify map displays correctly
   - Check probability gauge rendering
   - Test responsive design on mobile

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API endpoint
ab -n 1000 -c 10 http://localhost:8000/health
```

## 🚀 Deployment

### Production Build

**Build Docker Images**:
```bash
# Backend + Frontend (all-in-one)
docker build -t is-it-rain-api:latest --target backend .

# Frontend only
docker build -t is-it-rain-frontend:latest --target frontend .
```

### Deployment Options

#### 1. AWS (ECS + Fargate)
```bash
# Push to ECR
aws ecr create-repository --repository-name is-it-rain-api
docker tag is-it-rain-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest

# Deploy to ECS
aws ecs create-service --cluster my-cluster --service-name is-it-rain ...
```

#### 2. Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/is-it-rain-api
gcloud run deploy is-it-rain-api --image gcr.io/PROJECT-ID/is-it-rain-api --platform managed
```

#### 3. Azure App Service
```bash
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name is-it-rain-api \
  --deployment-container-image-name is-it-rain-api:latest
```

#### 4. Heroku
```bash
heroku container:push web -a is-it-rain-api
heroku container:release web -a is-it-rain-api
```

#### 5. Railway / Render / Fly.io
- Connect GitHub repository
- Select Dockerfile deployment
- Configure environment variables
- Deploy

**Complete Deployment Guide**: See `docs/DEPLOYMENT.md`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in `backend/` directory:

```bash
# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# NASA API Settings
NASA_TIMEOUT=15

# Cache Settings (seconds)
CACHE_TTL=900

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Database
DATABASE_ENABLED=true
DATABASE_PATH=data/forecasts.db

# Logging
LOG_LEVEL=INFO

# Optional: Proxy Settings
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=https://proxy.example.com:8080
```

### Customization

**Adjust Probability Thresholds** (`backend/app/services/nasa_power.py`):
```python
def _precipitation_probability(mm_value: float) -> float:
    # Customize these thresholds based on your needs
    if mm_value <= 0.2: return 0.1
    if mm_value <= 1: return 0.35
    # ... etc
```

**Modify Cache Duration** (`.env`):
```bash
CACHE_TTL=1800  # 30 minutes instead of 15
```

**Change Rate Limits** (`.env`):
```bash
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=5000
```

## 📁 Project Structure

```
Is-It-Rain/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes.py   # Forecast endpoints
│   │   ├── core/           # Core functionality
│   │   │   ├── cache.py    # Caching logic
│   │   │   ├── config.py   # Configuration
│   │   │   ├── database.py # Database operations
│   │   │   └── rate_limit.py # Rate limiting
│   │   ├── models/         # Pydantic models
│   │   │   └── forecast.py # Data models
│   │   ├── services/       # External services
│   │   │   ├── geocoding.py # OpenStreetMap
│   │   │   └── nasa_power.py # NASA API
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   ├── pyproject.toml      # Python dependencies
│   └── .env                # Environment variables
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── EventForm.tsx
│   │   │   ├── ForecastResult.tsx
│   │   │   ├── ForecastMap.tsx
│   │   │   └── ProbabilityGauge.tsx
│   │   ├── hooks/          # Custom hooks
│   │   │   └── useForecast.ts
│   │   ├── styles/         # CSS styles
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main component
│   │   └── main.tsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
│
├── infra/                  # Infrastructure
│   ├── docker-compose.yml  # Docker Compose config
│   └── README.md           # Infra documentation
│
├── docs/                   # Documentation
│   ├── API.md             # API documentation
│   ├── DEPLOYMENT.md      # Deployment guide
│   └── architecture.md    # Architecture details
│
├── data/                   # Data samples
│   ├── sample_imerg.json  # Sample NASA data
│   └── README.md          # Dataset information
│
├── Dockerfile             # Multi-stage build
└── README.md              # This file
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.11+
- **Package Manager**: Poetry
- **Database**: SQLite (upgradable to PostgreSQL)
- **Caching**: In-memory TTL cache (upgradable to Redis)
- **Logging**: Loguru
- **HTTP Client**: httpx (async)
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18.3
- **Build Tool**: Vite 5.3
- **Language**: TypeScript 5.4
- **Styling**: Tailwind CSS 3.4
- **Maps**: Leaflet 1.9 + React-Leaflet 4.2
- **Charts**: Recharts 2.12
- **State**: TanStack Query 5.51
- **Forms**: React Hook Form 7.51
- **Date Handling**: date-fns 3.6

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (optional)
- **Cloud**: AWS, Azure, GCP, Heroku

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `poetry run pytest` and `npm run lint`
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation
- Keep commits atomic and meaningful

## 📄 License

This project was created for the NASA Space Apps Challenge 2025.

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **NASA**: For providing the POWER API and GPM IMERG data
- **OpenStreetMap**: For geocoding services
- **NASA Space Apps Challenge 2025**: For the inspiration and challenge
- **Contributors**: Everyone who helped build this project

## 📞 Support

- **Issues**: https://github.com/Nabeel70/Is-It-Rain/issues
- **Documentation**: See `docs/` directory
- **NASA Space Apps**: https://www.spaceappschallenge.org/

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

## 📈 Roadmap

- [ ] Add weather forecast APIs for true future predictions
- [ ] Implement webhook notifications
- [ ] Add multi-day forecast view
- [ ] Support for additional precipitation metrics (snow, hail)
- [ ] Mobile app (React Native)
- [ ] Historical data visualization dashboard
- [ ] Machine learning models for improved predictions
- [ ] Integration with calendar apps
- [ ] Email/SMS notifications
- [ ] Public API with authentication

---

**Built with ❤️ for NASA Space Apps Challenge 2025**
   referencing NASA POWER documentation. Consider augmenting with IMERG
   half-hourly or ECMWF reanalysis for ensemble modeling.
6. Harden for production by enabling HTTPS, setting `ALLOWED_ORIGINS` to your
   domain, and deploying the Docker image to your chosen platform.
7. Monitor NASA and OpenStreetMap API quotas, add retries/backoff if your event
   load increases, and document operations in `docs/`.
