import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { ForecastRequest, ForecastResponse } from '../types/api';

async function postForecast(payload: ForecastRequest): Promise<ForecastResponse> {
  const { data } = await axios.post<ForecastResponse>('/api/forecast', payload);
  return data;
}

export function useForecast() {
  return useMutation({
    mutationKey: ['forecast'],
    mutationFn: postForecast
  });
}
