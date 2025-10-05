# API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication. For production use with authentication, add API keys or OAuth2.

## Rate Limiting

- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

Rate limit headers are included in responses:
- `X-RateLimit-Minute-Limit`
- `X-RateLimit-Minute-Remaining`
- `X-RateLimit-Hour-Limit`
- `X-RateLimit-Hour-Remaining`

## Endpoints

### Health Check

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok",
  "message": "Is It Rain API is running"
}
```

**Status Codes**:
- `200 OK`: API is healthy

---

### Get Forecast

Get precipitation forecast for a specific date and location.

**Endpoint**: `POST /api/forecast`

**Request Body**:
```json
{
  "event_date": "2025-12-25",
  "query": "Central Park, New York, NY"
}
```

OR with coordinates:

```json
{
  "event_date": "2025-12-25",
  "location": {
    "latitude": 40.785091,
    "longitude": -73.968285,
    "name": "Central Park"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_date` | string (ISO 8601 date) | Yes | Event date in format YYYY-MM-DD |
| `query` | string | Conditional* | Location search query (e.g., "Paris, France") |
| `location` | object | Conditional* | Location object with latitude/longitude |
| `location.latitude` | number | No | Latitude (-90 to 90) |
| `location.longitude` | number | No | Longitude (-180 to 180) |
| `location.name` | string | No | Optional location name |

*Either `query` or `location` must be provided.

**Response**:
```json
{
  "location": {
    "latitude": 40.785091,
    "longitude": -73.968285,
    "name": "Central Park, Manhattan, New York County, City of New York, New York, 10024, United States"
  },
  "event_date": "2025-12-25",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 2.5,
  "summary": "Low chance of rain; keep an eye on the sky. (Based on 2024 historical data)",
  "nasa_dataset": "NASA POWER (GPM IMERG derived) (Historical Proxy)",
  "issued_at": "2025-10-05T10:42:15.123456Z"
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `location` | object | Location information |
| `location.latitude` | number | Latitude of location |
| `location.longitude` | number | Longitude of location |
| `location.name` | string | Human-readable location name |
| `event_date` | string | Event date (YYYY-MM-DD) |
| `precipitation_probability` | number | Probability of measurable rain (0.0 to 1.0) |
| `precipitation_intensity_mm` | number | Expected precipitation in millimeters |
| `summary` | string | Human-readable forecast summary |
| `nasa_dataset` | string | Data source description |
| `issued_at` | string | Timestamp when forecast was generated (ISO 8601) |

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Location not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

**Example Requests**:

Using cURL:
```bash
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo, Japan"}'
```

Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/forecast",
    json={
        "event_date": "2025-12-25",
        "query": "Tokyo, Japan"
    }
)
print(response.json())
```

Using JavaScript:
```javascript
fetch('http://localhost:8000/api/forecast', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    event_date: '2025-12-25',
    query: 'Tokyo, Japan'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### Get Statistics

Get overall system statistics.

**Endpoint**: `GET /api/stats`

**Response**:
```json
{
  "total_forecasts": 1234,
  "avg_rain_probability": 0.456,
  "avg_precipitation_mm": 2.34,
  "unique_locations": 567
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `total_forecasts` | integer | Total number of forecasts generated |
| `avg_rain_probability` | number | Average rain probability across all forecasts |
| `avg_precipitation_mm` | number | Average precipitation in millimeters |
| `unique_locations` | integer | Number of unique locations queried |

**Status Codes**:
- `200 OK`: Success
- `503 Service Unavailable`: Database not enabled

---

### Get Forecast History

Get forecast history for a specific location.

**Endpoint**: `GET /api/history`

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `latitude` | number | Yes | Latitude of location |
| `longitude` | number | Yes | Longitude of location |
| `limit` | integer | No | Maximum number of results (default: 10) |

**Example Request**:
```bash
curl "http://localhost:8000/api/history?latitude=40.785091&longitude=-73.968285&limit=5"
```

**Response**:
```json
[
  {
    "id": 123,
    "latitude": 40.785091,
    "longitude": -73.968285,
    "location_name": "Central Park, Manhattan, ...",
    "event_date": "2025-12-25",
    "precipitation_probability": 0.35,
    "precipitation_intensity_mm": 2.5,
    "summary": "Low chance of rain...",
    "nasa_dataset": "NASA POWER (GPM IMERG derived)",
    "issued_at": "2025-10-05T10:42:15.123456Z",
    "created_at": "2025-10-05T10:42:15.123456Z"
  }
]
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid parameters
- `503 Service Unavailable`: Database not enabled

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Examples

**400 Bad Request**:
```json
{
  "detail": "Either location coordinates or query must be provided"
}
```

**404 Not Found**:
```json
{
  "detail": "Unable to geocode query: Nonexistent Place"
}
```

**429 Too Many Requests**:
```json
{
  "detail": "Rate limit exceeded: 60 requests per minute"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

---

## Data Sources

### NASA POWER API

The application uses NASA's POWER (Prediction Of Worldwide Energy Resources) API, which provides:

- **Parameter**: `PRECTOTCORR` (Corrected Total Precipitation)
- **Source**: GPM IMERG (Global Precipitation Measurement - Integrated Multi-satellitE Retrievals)
- **Resolution**: Daily precipitation totals
- **Coverage**: Global
- **Data Type**: Historical observations (not real-time forecasts)

**Important Note**: NASA POWER provides historical data, not future forecasts. For future dates, the API uses historical data from the same date in the previous year as a proxy estimate.

### OpenStreetMap Nominatim

Used for geocoding (converting place names to coordinates) and reverse geocoding (converting coordinates to place names).

- **Rate Limit**: 1 request per second (please be respectful)
- **Coverage**: Global
- **Attribution Required**: Yes (included in footer)

---

## Caching

The API implements intelligent caching to reduce load on external services:

- **Cache Duration**: 15 minutes (900 seconds) by default
- **Cache Key**: Based on location coordinates and date
- **Benefits**: Faster responses, reduced API calls to NASA POWER

---

## Best Practices

### 1. Handle Rate Limits

```python
import time
import requests

def get_forecast_with_retry(event_date, query, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(
            "http://localhost:8000/api/forecast",
            json={"event_date": event_date, "query": query}
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limited, wait and retry
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
        else:
            response.raise_for_status()
    
    raise Exception("Max retries exceeded")
```

### 2. Use Coordinates When Possible

Using coordinates is faster and more reliable than search queries:

```python
# Good: Direct coordinates
{"event_date": "2025-12-25", "location": {"latitude": 40.7128, "longitude": -74.0060}}

# Also good, but slower: Search query
{"event_date": "2025-12-25", "query": "New York, NY"}
```

### 3. Batch Requests Efficiently

Don't make multiple requests for the same location/date:

```python
# Bad: Multiple redundant requests
for _ in range(10):
    response = requests.post(..., json={"event_date": "2025-12-25", "query": "Paris"})

# Good: Make request once, reuse result
response = requests.post(..., json={"event_date": "2025-12-25", "query": "Paris"})
result = response.json()
# Use result multiple times
```

### 4. Handle Errors Gracefully

```python
try:
    response = requests.post("http://localhost:8000/api/forecast", json=data)
    response.raise_for_status()
    forecast = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Location not found")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

---

## Interactive API Documentation

FastAPI provides interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- View all endpoints
- Test API calls directly in the browser
- See request/response schemas
- Download OpenAPI specification

---

## Webhook Integration (Future)

For automated event monitoring, you can set up webhooks (to be implemented):

```json
POST /api/webhooks
{
  "url": "https://your-app.com/webhook",
  "event_date": "2025-12-25",
  "location": {"latitude": 40.7128, "longitude": -74.0060},
  "threshold": 0.5
}
```

This would notify your application when precipitation probability exceeds the threshold.

---

## SDK Examples

### Python SDK Example

```python
class IsItRainClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_forecast(self, event_date, query=None, location=None):
        payload = {"event_date": event_date}
        if query:
            payload["query"] = query
        elif location:
            payload["location"] = location
        else:
            raise ValueError("Either query or location required")
        
        response = requests.post(
            f"{self.base_url}/api/forecast",
            json=payload
        )
        response.raise_for_status()
        return response.json()

# Usage
client = IsItRainClient()
forecast = client.get_forecast("2025-12-25", query="Paris, France")
print(f"Rain probability: {forecast['precipitation_probability'] * 100}%")
```

### JavaScript SDK Example

```javascript
class IsItRainClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async getForecast(eventDate, options = {}) {
    const payload = { event_date: eventDate };
    
    if (options.query) {
      payload.query = options.query;
    } else if (options.location) {
      payload.location = options.location;
    } else {
      throw new Error('Either query or location required');
    }
    
    const response = await fetch(`${this.baseUrl}/api/forecast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }
}

// Usage
const client = new IsItRainClient();
const forecast = await client.getForecast('2025-12-25', { query: 'Paris, France' });
console.log(`Rain probability: ${forecast.precipitation_probability * 100}%`);
```

---

## Support

For questions, issues, or feature requests:

- **GitHub**: https://github.com/Nabeel70/Is-It-Rain/issues
- **Documentation**: See `/docs` directory
- **API Status**: Check `/health` endpoint

---

## Changelog

### Version 0.1.0 (2025-10-05)

- Initial release
- Basic forecast endpoint
- Statistics endpoint
- Forecast history endpoint
- Rate limiting
- Caching
- Database storage
