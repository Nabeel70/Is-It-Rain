# API Documentation

This document describes the REST API endpoints provided by the "Will It Rain On My Parade?" backend service.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com` (configure as needed)

## API Prefix

All endpoints are prefixed with `/api`

## Authentication

No authentication is required for any endpoints.

## Endpoints

### 1. Health Check

Check if the API service is running and healthy.

**Endpoint**: `GET /api/health`

**Response**:

```json
{
  "status": "ok",
  "timestamp": "2025-10-05T10:00:00.000000Z"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `500 Internal Server Error`: Service is down

**Example**:

```bash
curl http://localhost:8000/api/health
```

**Use Cases**:
- Load balancer health checks
- Monitoring and alerting
- Deployment validation

---

### 2. Get Forecast

Retrieve precipitation forecast for a specific location and date.

**Endpoint**: `POST /api/forecast`

**Request Body**:

```json
{
  "event_date": "2025-10-05",
  "query": "New York City, NY"
}
```

OR (with explicit coordinates):

```json
{
  "event_date": "2025-10-05",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "name": "New York City"
  }
}
```

**Request Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_date` | string (YYYY-MM-DD) | Yes | Date of the event |
| `query` | string | No* | Location query (free-form text) |
| `location` | object | No* | Explicit location coordinates |
| `location.latitude` | float | No* | Latitude (-90 to 90) |
| `location.longitude` | float | No* | Longitude (-180 to 180) |
| `location.name` | string | No | Human-readable location name |

*Either `query` OR `location` must be provided.

**Response**:

```json
{
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "name": "New York, New York, United States"
  },
  "event_date": "2025-10-05",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 0.8,
  "summary": "Low chance of rain; keep an eye on the sky.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:30:00.123456Z"
}
```

**Response Schema**:

| Field | Type | Description |
|-------|------|-------------|
| `location` | object | Location information |
| `location.latitude` | float | Latitude coordinate |
| `location.longitude` | float | Longitude coordinate |
| `location.name` | string | Human-readable location name |
| `event_date` | string | Date of the event (YYYY-MM-DD) |
| `precipitation_probability` | float | Probability of rain (0.0 to 1.0) |
| `precipitation_intensity_mm` | float | Expected precipitation in mm/day |
| `summary` | string | Human-readable forecast summary |
| `nasa_dataset` | string | Data source identifier |
| `issued_at` | string | Timestamp when forecast was generated (ISO 8601) |

**Status Codes**:
- `200 OK`: Forecast retrieved successfully
- `400 Bad Request`: Invalid request (missing location or invalid date)
- `404 Not Found`: Location not found or data unavailable
- `500 Internal Server Error`: Server error or external API failure

**Example Requests**:

1. **With location query**:
   ```bash
   curl -X POST http://localhost:8000/api/forecast \
     -H "Content-Type: application/json" \
     -d '{
       "event_date": "2025-10-05",
       "query": "San Francisco, CA"
     }'
   ```

2. **With coordinates**:
   ```bash
   curl -X POST http://localhost:8000/api/forecast \
     -H "Content-Type: application/json" \
     -d '{
       "event_date": "2025-10-05",
       "location": {
         "latitude": 37.7749,
         "longitude": -122.4194,
         "name": "San Francisco"
       }
     }'
   ```

3. **With JavaScript/TypeScript**:
   ```typescript
   const response = await fetch('http://localhost:8000/api/forecast', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({
       event_date: '2025-10-05',
       query: 'Central Park, New York, NY',
     }),
   });
   
   const forecast = await response.json();
   console.log(forecast);
   ```

4. **With Python**:
   ```python
   import requests
   
   response = requests.post(
       'http://localhost:8000/api/forecast',
       json={
           'event_date': '2025-10-05',
           'query': 'London, UK'
       }
   )
   
   forecast = response.json()
   print(forecast)
   ```

**Error Responses**:

1. **Missing location** (400):
   ```json
   {
     "detail": "Either location coordinates or query must be provided"
   }
   ```

2. **Location not found** (404):
   ```json
   {
     "detail": "Unable to geocode query: xyz123"
   }
   ```

3. **Invalid date format** (422):
   ```json
   {
     "detail": [
       {
         "loc": ["body", "event_date"],
         "msg": "invalid date format",
         "type": "value_error.date"
       }
     ]
   }
   ```

4. **Invalid coordinates** (422):
   ```json
   {
     "detail": [
       {
         "loc": ["body", "location", "latitude"],
         "msg": "ensure this value is greater than or equal to -90",
         "type": "value_error.number.not_ge"
       }
     ]
   }
   ```

**Use Cases**:
- Get precipitation forecast for outdoor events
- Plan parade or outdoor activity
- Check rain risk for specific date and location

---

## Caching

The API caches responses for 15 minutes (900 seconds) by default to:
- Reduce load on external APIs (NASA POWER, OpenStreetMap)
- Improve response times
- Respect rate limits

**Cache Key**: Based on location coordinates and date

**Cache Behavior**:
- First request: Fetches from external APIs (~2-5 seconds)
- Subsequent requests (within 15 min): Returns cached result (~50ms)
- After cache expiry: Fetches fresh data

**Cache Configuration**:

Set `CACHE_TTL` environment variable (in seconds):
```bash
CACHE_TTL=900  # 15 minutes (default)
CACHE_TTL=1800 # 30 minutes
CACHE_TTL=3600 # 1 hour
```

## Rate Limiting

The API itself does not enforce rate limits, but external APIs have their own limits:

- **NASA POWER API**: No official limits (be respectful)
- **OpenStreetMap Nominatim**: 1 request per second

**Recommendations**:
- Implement rate limiting at API gateway level
- Recommended: 100 requests/minute per IP
- Use caching to reduce external API calls

## CORS

Cross-Origin Resource Sharing (CORS) is configured via the `ALLOWED_ORIGINS` environment variable.

**Development**:
```bash
ALLOWED_ORIGINS=["http://localhost:5173"]
```

**Production**:
```bash
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

**Multiple Origins**:
```bash
ALLOWED_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
```

## Error Handling

All errors follow the FastAPI standard error response format:

```json
{
  "detail": "Error message here"
}
```

**Common Errors**:

| Status Code | Description | Cause |
|-------------|-------------|-------|
| 400 | Bad Request | Invalid input parameters |
| 404 | Not Found | Location not found or data unavailable |
| 422 | Unprocessable Entity | Validation error (invalid data format) |
| 500 | Internal Server Error | Server error or external API failure |
| 503 | Service Unavailable | External API temporarily unavailable |

## Request/Response Examples

### Example 1: Successful Forecast (Light Rain)

**Request**:
```json
POST /api/forecast
{
  "event_date": "2025-06-15",
  "query": "Seattle, WA"
}
```

**Response** (200 OK):
```json
{
  "location": {
    "latitude": 47.6062,
    "longitude": -122.3321,
    "name": "Seattle, King County, Washington, United States"
  },
  "event_date": "2025-06-15",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 0.6,
  "summary": "Low chance of rain; keep an eye on the sky.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:30:15.789012Z"
}
```

### Example 2: Successful Forecast (Heavy Rain)

**Request**:
```json
POST /api/forecast
{
  "event_date": "2025-07-20",
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "name": "Mumbai, India"
  }
}
```

**Response** (200 OK):
```json
{
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "name": "Mumbai, India"
  },
  "event_date": "2025-07-20",
  "precipitation_probability": 0.95,
  "precipitation_intensity_mm": 15.2,
  "summary": "Severe rain threat expected. Consider rescheduling or moving indoors.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:31:42.123456Z"
}
```

### Example 3: Location Not Found

**Request**:
```json
POST /api/forecast
{
  "event_date": "2025-10-05",
  "query": "Nonexistent Place XYZ123"
}
```

**Response** (404 Not Found):
```json
{
  "detail": "Unable to geocode query: Nonexistent Place XYZ123"
}
```

### Example 4: Missing Location

**Request**:
```json
POST /api/forecast
{
  "event_date": "2025-10-05"
}
```

**Response** (400 Bad Request):
```json
{
  "detail": "Either location coordinates or query must be provided"
}
```

### Example 5: Invalid Coordinates

**Request**:
```json
POST /api/forecast
{
  "event_date": "2025-10-05",
  "location": {
    "latitude": 999,
    "longitude": -74.0060
  }
}
```

**Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "location", "latitude"],
      "msg": "Input should be less than or equal to 90",
      "input": 999,
      "ctx": {
        "le": 90
      }
    }
  ]
}
```

## OpenAPI / Swagger Documentation

The API provides interactive documentation via Swagger UI:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

These pages provide:
- Interactive API testing
- Request/response schemas
- Example requests
- Try it out functionality

## Client Libraries

### TypeScript/JavaScript

```typescript
// types/api.ts
export interface Location {
  latitude: number;
  longitude: number;
  name?: string;
}

export interface ForecastRequest {
  event_date: string;
  query?: string;
  location?: Location;
}

export interface ForecastResponse {
  location: Location;
  event_date: string;
  precipitation_probability: number;
  precipitation_intensity_mm: number;
  summary: string;
  nasa_dataset: string;
  issued_at: string;
}

// client.ts
export class RainForecastClient {
  constructor(private baseUrl: string) {}

  async getForecast(request: ForecastRequest): Promise<ForecastResponse> {
    const response = await fetch(`${this.baseUrl}/api/forecast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Forecast request failed');
    }

    return response.json();
  }

  async checkHealth(): Promise<{ status: string; timestamp: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);
    return response.json();
  }
}

// Usage
const client = new RainForecastClient('http://localhost:8000');
const forecast = await client.getForecast({
  event_date: '2025-10-05',
  query: 'New York City',
});
```

### Python

```python
from typing import Optional
from datetime import date
import requests


class RainForecastClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_forecast(
        self,
        event_date: date,
        query: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        name: Optional[str] = None,
    ) -> dict:
        """Get precipitation forecast for a location and date."""
        payload = {"event_date": event_date.isoformat()}
        
        if query:
            payload["query"] = query
        elif latitude is not None and longitude is not None:
            payload["location"] = {
                "latitude": latitude,
                "longitude": longitude,
            }
            if name:
                payload["location"]["name"] = name
        else:
            raise ValueError("Either query or coordinates must be provided")

        response = requests.post(
            f"{self.base_url}/api/forecast",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def check_health(self) -> dict:
        """Check API health status."""
        response = requests.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        return response.json()


# Usage
client = RainForecastClient()
forecast = client.get_forecast(
    event_date=date(2025, 10, 5),
    query="New York City",
)
print(f"Probability: {forecast['precipitation_probability']:.0%}")
print(f"Summary: {forecast['summary']}")
```

## Best Practices

### For Clients

1. **Error Handling**
   - Always handle HTTP errors
   - Parse error messages from `detail` field
   - Implement retry logic with exponential backoff

2. **Caching**
   - Cache responses on client side
   - Respect cache headers
   - Don't hammer the API with repeated requests

3. **Input Validation**
   - Validate date format before sending
   - Validate coordinate ranges
   - Provide specific location queries

4. **Timeouts**
   - Set reasonable timeouts (10-30 seconds)
   - External API calls can be slow
   - Handle timeout gracefully

5. **Rate Limiting**
   - Implement client-side rate limiting
   - Respect 429 responses (if implemented)
   - Use exponential backoff

### For API Operators

1. **Monitoring**
   - Monitor `/api/health` endpoint
   - Track response times
   - Alert on error rates > 1%

2. **Logging**
   - Log all external API calls
   - Log errors with stack traces
   - Monitor NASA API quota

3. **Security**
   - Configure CORS properly
   - Use HTTPS in production
   - Implement rate limiting

4. **Performance**
   - Monitor cache hit rates
   - Optimize slow queries
   - Scale horizontally if needed

## Changelog

- **2025-10-05**: Initial API documentation

---

For more information, see:
- [README.md](../README.md) - Project overview
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- [DATASETS.md](./DATASETS.md) - Dataset documentation

Last Updated: October 5, 2025
