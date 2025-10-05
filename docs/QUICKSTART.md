# Quick Start Guide

Get the "Will It Rain On My Parade?" application running in minutes!

## Prerequisites

Choose one method:

### Method 1: Docker (Easiest)
- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+

### Method 2: Manual Setup
- Python 3.11+
- Node.js 20+
- Poetry (Python package manager)
- npm 10+

## Installation

### Option A: Docker (Recommended for Quick Start)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Nabeel70/Is-It-Rain.git
   cd Is-It-Rain
   ```

2. **Start the Application**
   ```bash
   cd infra
   docker compose up --build
   ```

   This command will:
   - Build frontend and backend Docker images
   - Start both services
   - Set up networking between them

3. **Access the Application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the Application**
   ```bash
   # Press Ctrl+C in the terminal
   # Or in another terminal:
   docker compose down
   ```

**Troubleshooting Docker**:
- Port conflicts: Change ports in `infra/docker-compose.yml`
- Build errors: Run `docker compose build --no-cache`
- Network issues: Run `docker compose down -v` then retry

### Option B: Manual Setup (Development)

#### Step 1: Clone Repository

```bash
git clone https://github.com/Nabeel70/Is-It-Rain.git
cd Is-It-Rain
```

#### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Poetry (if not already installed)
pip install poetry

# Install dependencies
poetry install

# Configure environment variables
cp .env.example .env

# (Optional) Edit .env file if needed
# nano .env

# Start the backend server
poetry run uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

**Verify Backend**:
```bash
curl http://localhost:8000/api/health
# Expected: {"status":"ok","timestamp":"..."}
```

#### Step 3: Frontend Setup

Open a **new terminal**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at http://localhost:5173

**Verify Frontend**:
Open http://localhost:5173 in your browser. You should see the application.

## First Run

### Testing the Application

1. **Open the Frontend**
   - Navigate to http://localhost:5173

2. **Enter Event Details**
   - **Location**: Try "New York City, NY" or "San Francisco, CA"
   - **Date**: Select any date (e.g., today's date)

3. **Submit the Form**
   - Click "Get Forecast" button
   - Wait 2-3 seconds for the response

4. **View Results**
   - See precipitation probability
   - View location on the map
   - Check the forecast summary

### Example API Call

Test the backend directly:

```bash
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "event_date": "2025-10-05",
    "query": "London, UK"
  }'
```

Expected response:
```json
{
  "location": {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "name": "London, United Kingdom"
  },
  "event_date": "2025-10-05",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 0.8,
  "summary": "Low chance of rain; keep an eye on the sky.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:00:00.000000Z"
}
```

## Configuration

### Environment Variables

Backend configuration (`.env` file):

```bash
# CORS origins (JSON array format)
ALLOWED_ORIGINS=["http://localhost:5173"]

# Optional: HTTP/HTTPS proxy
HTTP_PROXY=
HTTPS_PROXY=

# NASA API timeout (seconds)
NASA_TIMEOUT=15

# Cache TTL (seconds)
CACHE_TTL=900
```

**Important**: `ALLOWED_ORIGINS` must be a JSON array:
```bash
# ✅ Correct
ALLOWED_ORIGINS=["http://localhost:5173"]
ALLOWED_ORIGINS=["http://localhost:5173","https://yourdomain.com"]

# ❌ Incorrect
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend Configuration

The frontend uses Vite's proxy for API calls. No configuration needed for local development.

For production, update the API base URL in your deployment configuration.

## Common Issues

### Issue 1: Port Already in Use

**Error**: `Address already in use` or `Port 8000 is already allocated`

**Solution**:
```bash
# Find process using the port
lsof -i :8000  # or :5173 for frontend

# Kill the process
kill -9 <PID>

# Or use different ports
# Backend: uvicorn app.main:app --port 8001
# Frontend: Edit vite.config.ts to change port
```

### Issue 2: CORS Errors

**Error**: `Access-Control-Allow-Origin` error in browser console

**Solution**:
1. Check `backend/.env` file
2. Ensure `ALLOWED_ORIGINS` includes your frontend URL
3. Format must be JSON array: `["http://localhost:5173"]`
4. Restart backend server after changes

### Issue 3: NASA API Errors

**Error**: `500 Internal Server Error` when requesting forecast

**Solution**:
1. Check internet connection
2. Verify NASA POWER API is accessible: https://power.larc.nasa.gov/
3. Increase timeout in `.env`: `NASA_TIMEOUT=30`
4. Check logs for detailed error message

### Issue 4: Geocoding Fails

**Error**: `Unable to geocode query: <location>`

**Solution**:
1. Be more specific with location: "New York City, NY" instead of "NYC"
2. Check OpenStreetMap Nominatim is accessible: https://nominatim.openstreetmap.org/
3. Try using coordinates instead:
   ```json
   {
     "event_date": "2025-10-05",
     "location": {
       "latitude": 40.7128,
       "longitude": -74.0060
     }
   }
   ```

### Issue 5: Dependencies Not Installing

**Backend**:
```bash
# Clear cache and reinstall
poetry cache clear . --all
poetry install
```

**Frontend**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Workflow

### Making Changes

1. **Backend Changes**
   - Edit files in `backend/app/`
   - Server auto-reloads (--reload flag)
   - Check http://localhost:8000/docs for updated API

2. **Frontend Changes**
   - Edit files in `frontend/src/`
   - Browser auto-reloads
   - Check browser console for errors

3. **Testing Changes**
   ```bash
   # Backend tests
   cd backend
   poetry run pytest
   
   # Frontend linting
   cd frontend
   npm run lint
   ```

### Debugging

**Backend**:
- Check terminal logs for error messages
- Use `/api/health` endpoint to verify server is running
- Check `backend/app/main.py` for application startup

**Frontend**:
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed API calls
- Use React DevTools extension for component debugging

## Next Steps

Once you have the application running:

1. **Explore the Code**
   - Backend: `backend/app/`
   - Frontend: `frontend/src/`
   - Documentation: `docs/`

2. **Read Documentation**
   - [API Documentation](API.md) - REST API reference
   - [Dataset Documentation](DATASETS.md) - Data sources
   - [Architecture](architecture.md) - System design

3. **Try Development Tasks**
   - Add a new feature
   - Improve UI/UX
   - Add tests
   - Update documentation

4. **Deploy to Production**
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options

## Learning Resources

### Backend (Python/FastAPI)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)

### Frontend (React/TypeScript)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)

### APIs
- [NASA POWER API](https://power.larc.nasa.gov/docs/)
- [OpenStreetMap Nominatim](https://nominatim.org/release-docs/latest/)

## Support

Need help? Here's how to get support:

1. **Check Documentation**
   - Read [README.md](../README.md)
   - Check [API.md](API.md) for API questions
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

2. **Search Issues**
   - Check [existing issues](https://github.com/Nabeel70/Is-It-Rain/issues)
   - Someone may have had the same problem

3. **Ask Questions**
   - Open a [GitHub Discussion](https://github.com/Nabeel70/Is-It-Rain/discussions)
   - Or create a [new issue](https://github.com/Nabeel70/Is-It-Rain/issues/new)

4. **Report Bugs**
   - Use the [bug report template](https://github.com/Nabeel70/Is-It-Rain/issues/new?template=bug_report.md)
   - Include error messages and steps to reproduce

## Quick Reference

### Useful Commands

```bash
# Backend
cd backend
poetry install                    # Install dependencies
poetry run uvicorn app.main:app --reload  # Start dev server
poetry run pytest                 # Run tests
poetry run ruff check .           # Lint code

# Frontend
cd frontend
npm install                       # Install dependencies
npm run dev                       # Start dev server
npm run build                     # Build for production
npm run lint                      # Lint code

# Docker
cd infra
docker compose up --build         # Build and start
docker compose down               # Stop
docker compose logs               # View logs
docker compose ps                 # List containers
```

### Important URLs

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/api/health

### File Structure

```
Is-It-Rain/
├── backend/          # Python FastAPI backend
│   ├── app/          # Application code
│   ├── tests/        # Tests
│   └── .env          # Environment config
├── frontend/         # React frontend
│   ├── src/          # Source code
│   └── public/       # Static assets
├── docs/             # Documentation
├── infra/            # Docker setup
└── data/             # Sample data
```

---

**Ready to build?** Check out [CONTRIBUTING.md](../CONTRIBUTING.md) to start contributing!

**Questions?** Open an issue on [GitHub](https://github.com/Nabeel70/Is-It-Rain/issues)
