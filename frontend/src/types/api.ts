export interface Location {
  latitude: number;
  longitude: number;
  name?: string | null;
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

export interface ForecastRequest {
  event_date: string;
  query?: string;
  location?: Location;
}
