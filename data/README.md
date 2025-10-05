# Dataset Strategy

This project leverages NASA's POWER API, which provides daily surface meteorology
and solar energy parameters derived from satellite observations including the
GPM IMERG precipitation product. For detailed documentation, see:
https://power.larc.nasa.gov/

Key parameter: `PRECTOTCORR` (corrected total precipitation), expressed in
millimeters per day for the requested coordinate.

## Access instructions

1. No authentication is required for NASA POWER. You may call the REST endpoint:
   `https://power.larc.nasa.gov/api/temporal/daily/point` with parameters
   `latitude`, `longitude`, `start`, `end`, and `parameters=PRECTOTCORR`.
2. For higher temporal resolution (hourly) or more advanced analytics, consider
   staging data in a cloud bucket such as NASA's GES DISC via the Earthdata
   login.
3. Complementary geospatial context is provided by OpenStreetMap Nominatim
   reverse geocoding.

A sample request is included in `sample_imerg.json` for reference.
