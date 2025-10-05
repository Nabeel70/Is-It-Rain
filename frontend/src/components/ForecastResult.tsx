import { format } from 'date-fns';
import { ForecastResponse } from '../types/api';
import { ProbabilityGauge } from './ProbabilityGauge';
import { ForecastMap } from './ForecastMap';

interface ForecastResultProps {
  forecast: ForecastResponse;
}

export function ForecastResult({ forecast }: ForecastResultProps) {
  const eventDate = format(new Date(forecast.event_date), 'eeee, MMMM d, yyyy');
  const issuedAt = format(new Date(forecast.issued_at), 'PPPp');

  return (
    <div className="bg-slate-900/70 rounded-xl p-6 shadow-xl flex flex-col gap-6">
      <div className="flex flex-col lg:flex-row gap-6">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-white">Rain outlook</h3>
          <p className="text-sm text-slate-300">{eventDate}</p>
          <p className="mt-4 text-lg text-slate-100">{forecast.summary}</p>
          <div className="mt-3 bg-slate-800/40 border border-slate-700/50 rounded-lg px-3 py-2">
            <p className="text-xs text-slate-400">
              <strong>Data Source:</strong> {forecast.nasa_dataset}
            </p>
            <p className="text-xs text-slate-400 mt-1">
              {forecast.nasa_dataset.includes('Historical Proxy') ? (
                <>
                  ⚠️ Future date: Using last year&apos;s satellite observations as seasonal estimate
                </>
              ) : (
                <>
                  ✓ Historical date: Real satellite measurements from GPM IMERG
                </>
              )}
            </p>
            <p className="text-xs text-slate-500 mt-1">Issued: {issuedAt}</p>
          </div>
        </div>
        <div className="flex-1">
          <ProbabilityGauge probability={forecast.precipitation_probability} />
        </div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800">
          <h4 className="text-sm uppercase tracking-wide text-slate-400">Location</h4>
          <p className="text-lg font-medium text-slate-100">{forecast.location.name ?? 'Selected location'}</p>
          <p className="text-sm text-slate-400">
            lat {forecast.location.latitude.toFixed(3)}, lon {forecast.location.longitude.toFixed(3)}
          </p>
          <p className="text-sm text-slate-300 mt-2">
            Expected precipitation: {forecast.precipitation_intensity_mm.toFixed(1)} mm
          </p>
        </div>
        <ForecastMap location={forecast.location} />
      </div>
    </div>
  );
}
