import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { ForecastRequest, ForecastResponse } from '../types/api';

const RAW_API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const API_BASE_WITH_PROTOCOL = /^https?:\/\//i.test(RAW_API_BASE_URL)
  ? RAW_API_BASE_URL
  : `https://${RAW_API_BASE_URL}`;
const NORMALIZED_API_BASE_URL = API_BASE_WITH_PROTOCOL.replace(/\/$/, '');
const FORECAST_ENDPOINT = NORMALIZED_API_BASE_URL.endsWith('/api')
  ? `${NORMALIZED_API_BASE_URL}/forecast/ensemble`
  : `${NORMALIZED_API_BASE_URL}/api/forecast/ensemble`;

async function postForecast(payload: ForecastRequest): Promise<ForecastResponse> {
  const { data } = await axios.post<ForecastResponse>(FORECAST_ENDPOINT, payload);
  return data;
}

export function useForecast() {
  return useMutation({
    mutationKey: ['forecast'],
    mutationFn: postForecast
  });
}
