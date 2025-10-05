# Dataset Documentation

This document provides detailed information about the datasets used in the "Will It Rain On My Parade?" application.

## Overview

The application integrates multiple NASA Earth observation datasets and geocoding services to provide accurate precipitation forecasts for outdoor events.

## Primary Data Source: NASA POWER API

### What is NASA POWER?

NASA's Prediction Of Worldwide Energy Resources (POWER) project provides solar and meteorological data from NASA research for support of renewable energy, building energy efficiency, and agricultural needs.

**Official Documentation**: https://power.larc.nasa.gov/

### Dataset: GPM IMERG (Precipitation)

**Parameter Used**: `PRECTOTCORR` (Precipitation Corrected)

- **Full Name**: Global Precipitation Measurement (GPM) Integrated Multi-satellitE Retrievals for GPM (IMERG)
- **Description**: Corrected total precipitation at the surface of the Earth in millimeters per day
- **Spatial Resolution**: 0.5° x 0.5° (approximately 50km x 50km at equator)
- **Temporal Resolution**: Daily
- **Coverage**: Global (-90° to 90° latitude, -180° to 180° longitude)
- **Temporal Range**: June 1, 2000 to present (with 2-3 month lag for final product)
- **Update Frequency**: Daily (for near-real-time data)
- **Data Source**: Derived from GPM satellite constellation
- **Units**: mm/day

### How We Use It

1. **Request Format**
   ```
   GET https://power.larc.nasa.gov/api/temporal/daily/point?
       parameters=PRECTOTCORR
       &community=RE
       &longitude={lon}
       &latitude={lat}
       &start={YYYYMMDD}
       &end={YYYYMMDD}
       &format=JSON
   ```

2. **Response Format**
   ```json
   {
     "properties": {
       "parameter": {
         "PRECTOTCORR": {
           "20251005": 2.34
         }
       }
     }
   }
   ```

3. **Interpretation**
   - Value: Precipitation amount in mm/day
   - `0.0 - 0.2 mm`: Very light or no rain (10% probability)
   - `0.2 - 1.0 mm`: Light rain (35% probability)
   - `1.0 - 5.0 mm`: Moderate rain (60% probability)
   - `5.0 - 10.0 mm`: Heavy rain (80% probability)
   - `> 10.0 mm`: Very heavy rain (95% probability)

### Access and Authentication

- **Authentication**: None required
- **Rate Limits**: No official limits, but please be respectful
- **Cost**: Free
- **Registration**: Not required
- **Terms of Use**: https://power.larc.nasa.gov/docs/services/api/

### Data Quality and Limitations

**Strengths**:
- Global coverage
- Free and open access
- Well-documented
- Regularly updated
- Based on satellite observations

**Limitations**:
- 0.5° spatial resolution (not city-level precision)
- Daily temporal resolution (no hourly forecasts)
- 2-3 month lag for final validated data
- Historical data focus (not predictive forecasting)
- Best for planning past events, less reliable for future predictions

**Important Note**: NASA POWER provides historical and near-real-time data, NOT future forecasts. For future event dates, the application retrieves the most recent available data as a reference, but this should not be considered a weather forecast.

## Secondary Data Source: OpenStreetMap Nominatim

### What is Nominatim?

Nominatim is a geocoding service that converts location names to coordinates and vice versa, powered by OpenStreetMap data.

**Official Documentation**: https://nominatim.org/

### How We Use It

1. **Geocoding (Location Name → Coordinates)**
   ```
   GET https://nominatim.openstreetmap.org/search?
       q=New+York+City
       &format=json
       &limit=1
   ```

   Response:
   ```json
   [{
     "lat": "40.7127281",
     "lon": "-74.0060152",
     "display_name": "New York, United States"
   }]
   ```

2. **Reverse Geocoding (Coordinates → Location Name)**
   ```
   GET https://nominatim.openstreetmap.org/reverse?
       lat=40.7128
       &lon=-74.0060
       &format=json
       &zoom=14
   ```

   Response:
   ```json
   {
     "display_name": "New York, New York, United States"
   }
   ```

### Access and Authentication

- **Authentication**: None required
- **Rate Limits**: 1 request per second
- **Cost**: Free
- **Registration**: Not required
- **Terms of Use**: https://operations.osmfoundation.org/policies/nominatim/

### Usage Policy

**Must Do**:
- Include User-Agent header identifying your application
- Respect rate limits (1 req/sec)
- Cache results to reduce load

**Must Not**:
- Use for heavy batch geocoding
- Use for real-time tracking
- Resell the service

**Best Practices**:
- Cache geocoding results (we cache for 15 minutes)
- Use specific queries ("New York City, NY" not "NYC")
- Handle rate limit errors gracefully

## Additional Dataset Options (Future Enhancements)

### 1. IMERG Half-Hourly Data

For higher temporal resolution:

- **Source**: NASA GES DISC (https://disc.gsfc.nasa.gov/)
- **Resolution**: 30 minutes, 0.1° x 0.1°
- **Access**: Requires Earthdata login
- **Use Case**: Hourly precipitation tracking, event-level forecasting
- **Implementation**: Download HDF5 files, process with Python (h5py)

**Example Code**:
```python
import h5py
import numpy as np

# Read IMERG HDF5 file
with h5py.File('3B-HHR.MS.MRG.3IMERG.20251005-S000000-E002959.0000.V07B.HDF5', 'r') as f:
    precip = f['Grid']['precipitationCal'][:]
    lat = f['Grid']['lat'][:]
    lon = f['Grid']['lon'][:]
```

### 2. MERRA-2 Reanalysis

For atmospheric context:

- **Source**: NASA GMAO (https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/)
- **Variables**: Temperature, humidity, wind, pressure, clouds
- **Resolution**: 0.5° x 0.625°, hourly
- **Access**: Requires Earthdata login
- **Use Case**: Comprehensive weather analysis, model training
- **Format**: NetCDF files

### 3. MODIS Cloud Data

For cloud cover analysis:

- **Source**: NASA LAADS DAAC (https://ladsweb.modaps.eosdis.nasa.gov/)
- **Product**: MOD06 (Cloud Product)
- **Resolution**: 1km or 5km
- **Use Case**: Cloud coverage prediction, visibility
- **Format**: HDF-EOS files

### 4. GPM Ground Validation

For calibration and validation:

- **Source**: NASA GPM Ground Validation (https://gpm-gv.gsfc.nasa.gov/)
- **Data**: Ground radar, rain gauge measurements
- **Use Case**: Model validation, accuracy improvement
- **Access**: Public FTP server

## Data Pipeline Architecture

### Current Implementation

```
User Input (Location + Date)
    ↓
Geocoding (Nominatim)
    ↓
Location Coordinates
    ↓
NASA POWER API Query
    ↓
Precipitation Data (mm/day)
    ↓
Risk Calculation (Heuristic)
    ↓
Forecast Response
```

### Future Enhancement Options

1. **Multi-Model Ensemble**
   ```
   IMERG + MERRA-2 + MODIS → ML Model → Forecast
   ```

2. **Time Series Analysis**
   ```
   Historical Data (30 days) → Trend Analysis → Forecast
   ```

3. **Weather API Integration**
   ```
   NASA Data + Commercial API (OpenWeatherMap) → Ensemble
   ```

## Data Processing and Storage

### Current Approach

- **Processing**: Real-time API calls
- **Storage**: In-memory cache (15 minutes TTL)
- **Format**: JSON responses

### Scaling Options

1. **Database Storage**
   - PostgreSQL with PostGIS extension
   - Store historical forecasts
   - Enable analytics and reporting

2. **Data Lake**
   - S3/Azure Blob for raw data
   - Parquet format for efficient queries
   - Spark for batch processing

3. **Stream Processing**
   - Kafka for real-time data ingestion
   - Flink/Spark Streaming for processing
   - Redis for low-latency cache

## Sample Queries and Responses

### Example 1: Light Rain Event

**Input**:
- Location: San Francisco, CA
- Date: 2025-06-15
- Coordinates: (37.7749, -122.4194)

**NASA POWER Response**:
```json
{
  "PRECTOTCORR": {
    "20250615": 0.5
  }
}
```

**Application Response**:
```json
{
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "name": "San Francisco, California, United States"
  },
  "event_date": "2025-06-15",
  "precipitation_probability": 0.35,
  "precipitation_intensity_mm": 0.5,
  "summary": "Low chance of rain; keep an eye on the sky.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:00:00Z"
}
```

### Example 2: Heavy Rain Event

**Input**:
- Location: Mumbai, India
- Date: 2025-07-20
- Coordinates: (19.0760, 72.8777)

**NASA POWER Response**:
```json
{
  "PRECTOTCORR": {
    "20250720": 12.3
  }
}
```

**Application Response**:
```json
{
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "name": "Mumbai, Maharashtra, India"
  },
  "event_date": "2025-07-20",
  "precipitation_probability": 0.95,
  "precipitation_intensity_mm": 12.3,
  "summary": "Severe rain threat expected. Consider rescheduling or moving indoors.",
  "nasa_dataset": "NASA POWER (GPM IMERG PRECTOTCORR)",
  "issued_at": "2025-10-05T10:00:00Z"
}
```

## Data Quality Assurance

### Validation Steps

1. **Input Validation**
   - Latitude: -90 to 90
   - Longitude: -180 to 180
   - Date: Valid format (YYYY-MM-DD)

2. **API Response Validation**
   - Check HTTP status codes
   - Validate JSON structure
   - Handle missing data gracefully

3. **Data Sanity Checks**
   - Precipitation values ≥ 0
   - Reasonable ranges (0-500 mm/day)
   - Flag outliers for review

4. **Cache Validation**
   - Verify cache freshness (15 min TTL)
   - Check cache size limits
   - Handle cache misses

### Error Handling

1. **NASA API Errors**
   - Timeout: Retry with exponential backoff
   - 404: Return "data not available" message
   - 500: Log error, return generic error message

2. **Geocoding Errors**
   - No results: Prompt user for more specific location
   - Multiple results: Use first result
   - Rate limit: Implement queuing or fallback

3. **Data Gaps**
   - Missing dates: Return nearest available date
   - Invalid coordinates: Return error with guidance
   - Network errors: Return cached data if available

## Best Practices for Data Usage

### For Developers

1. **Caching**
   - Cache all API responses (15 min default)
   - Cache geocoding results indefinitely
   - Use Redis for distributed systems

2. **Rate Limiting**
   - Implement client-side rate limiting
   - Use exponential backoff for retries
   - Monitor API usage metrics

3. **Error Handling**
   - Always handle API failures gracefully
   - Provide meaningful error messages
   - Log all external API calls

4. **Testing**
   - Mock API responses in unit tests
   - Test with various locations and dates
   - Test error scenarios

### For Users

1. **Location Input**
   - Be specific: "Central Park, New York, NY" not "park"
   - Include city and state/country
   - Use official place names

2. **Date Selection**
   - Historical data is most accurate
   - Recent dates may have delays (2-3 months)
   - Future dates show reference data only

3. **Interpreting Results**
   - Probability is based on historical patterns
   - Not a real-time weather forecast
   - Use as planning tool, not absolute prediction

## Data Attribution and Citation

### NASA POWER

**Citation**:
```
NASA/POWER CERES/MERRA2 Native Resolution Daily Data
Dates: 20251005
Location: Latitude 40.7128, Longitude -74.0060
Elevation from MERRA-2: Average for 1/2x1/2 degree lat/lon region
Climate Zone: Humid Subtropical (Köppen-Geiger: Cfa)
Value for Missing Model Data: -999
Parameter(s): PRECTOTCORR

NASA/POWER SRB/FLASHFlux/MERRA2/GEOS 5.12.4 (FP-IT)
Dates (month/day/year): 01/01/2000 through 10/05/2025
Source: NASA/POWER
https://power.larc.nasa.gov/
```

### OpenStreetMap

**Attribution**:
```
© OpenStreetMap contributors
Data is available under the Open Database License
https://www.openstreetmap.org/copyright
```

### GPM

**Citation**:
```
Huffman, G.J., E.F. Stocker, D.T. Bolvin, E.J. Nelkin, Jackson Tan (2019),
GPM IMERG Final Precipitation L3 1 day 0.1 degree x 0.1 degree V06,
Greenbelt, MD, Goddard Earth Sciences Data and Information Services Center (GES DISC),
Accessed: [Data Access Date], 10.5067/GPM/IMERGDF/DAY/06
```

## Further Resources

### NASA POWER
- **Website**: https://power.larc.nasa.gov/
- **API Docs**: https://power.larc.nasa.gov/docs/services/api/
- **Data Dictionary**: https://power.larc.nasa.gov/docs/methodology/
- **User Community**: https://power.larc.nasa.gov/forum/

### GPM Mission
- **Website**: https://gpm.nasa.gov/
- **Data Access**: https://gpm.nasa.gov/data/directory
- **Publications**: https://gpm.nasa.gov/resources/publications
- **Education**: https://gpm.nasa.gov/education

### OpenStreetMap
- **Website**: https://www.openstreetmap.org/
- **Nominatim**: https://nominatim.org/
- **API Usage**: https://operations.osmfoundation.org/policies/nominatim/
- **Wiki**: https://wiki.openstreetmap.org/

### General Resources
- **NASA Earthdata**: https://www.earthdata.nasa.gov/
- **GES DISC**: https://disc.gsfc.nasa.gov/
- **Space Apps Challenge**: https://www.spaceappschallenge.org/

## Support and Questions

For questions about:
- **NASA POWER API**: Use their contact form at https://power.larc.nasa.gov/contact/
- **OpenStreetMap**: See https://help.openstreetmap.org/
- **This Application**: Open an issue on GitHub

## Changelog

- **2025-10-05**: Initial documentation
- Future updates will be documented here

---

Last Updated: October 5, 2025
