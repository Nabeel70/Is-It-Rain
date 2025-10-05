import { Controller, useForm } from 'react-hook-form';
import { format, parseISO } from 'date-fns';
import { ForecastRequest } from '../types/api';

interface EventFormProps {
  onSubmit: (payload: ForecastRequest) => void;
  isLoading: boolean;
}

const today = format(new Date(), 'yyyy-MM-dd');
const maxDate = format(new Date(new Date().setFullYear(new Date().getFullYear() + 1)), 'yyyy-MM-dd');

export function EventForm({ onSubmit, isLoading }: EventFormProps) {
  const { control, handleSubmit } = useForm<ForecastRequest>({
    defaultValues: {
      event_date: today,
      query: ''
    }
  });

  const submit = (values: ForecastRequest) => {
    onSubmit({
      event_date: format(parseISO(values.event_date), 'yyyy-MM-dd'),
      query: values.query?.trim()
    });
  };

  return (
    <form
      onSubmit={handleSubmit(submit)}
      className="bg-slate-900/70 backdrop-blur rounded-xl p-6 flex flex-col gap-4 shadow-xl"
    >
      <h2 className="text-2xl font-semibold">Plan your event</h2>
      <p className="text-sm text-slate-300">
        Pick a date and describe where your celebration takes place. We will combine NASA Earth
        observation data with open geospatial insights to estimate the chance of rain.
      </p>

      <label className="flex flex-col gap-2">
        <span className="text-sm font-medium text-slate-200">Event date</span>
        <Controller
          name="event_date"
          control={control}
          render={({ field }) => (
            <input
              {...field}
              type="date"
              min={today}
              max={maxDate}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-sky-500"
              required
            />
          )}
        />
      </label>

      <label className="flex flex-col gap-2">
        <span className="text-sm font-medium text-slate-200">Location</span>
        <Controller
          name="query"
          control={control}
          render={({ field }) => (
            <input
              {...field}
              type="text"
              placeholder="Central Park, New York"
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-sky-500"
              required
            />
          )}
        />
      </label>

      <button
        type="submit"
        disabled={isLoading}
        className="inline-flex justify-center items-center bg-sky-500 hover:bg-sky-400 text-white font-semibold py-2.5 rounded-lg transition disabled:opacity-50"
      >
        {isLoading ? 'Crunching satellite data…' : 'Will it rain?'}
      </button>
    </form>
  );
}
