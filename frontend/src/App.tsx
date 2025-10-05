import { useMemo } from 'react';
import { format } from 'date-fns';
import { EventForm } from './components/EventForm';
import { ForecastResult } from './components/ForecastResult';
import { useForecast } from './hooks/useForecast';

function App() {
  const { mutate, data, isPending, isError, error } = useForecast();

  const handleSubmit = (payload: { event_date: string; query?: string }) => {
    mutate(payload);
  };

  const todayLabel = useMemo(() => format(new Date(), 'PPP'), []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <header className="max-w-5xl mx-auto px-4 pt-16 pb-10 text-center">
        <h1 className="text-4xl md:text-5xl font-black tracking-tight text-white">
          Will It Rain On My Parade?
        </h1>
        <p className="mt-4 text-lg text-slate-300 max-w-3xl mx-auto">
          Powered by NASA GPM IMERG satellite data, this app shows historical precipitation patterns to help plan outdoor events.
        </p>
        <div className="mt-3 max-w-2xl mx-auto bg-blue-950/40 border border-blue-800/50 rounded-lg px-4 py-3">
          <p className="text-sm text-blue-200">
            <strong className="font-semibold">ℹ️ Data Source:</strong> Uses real NASA satellite observations (not forecasts). 
            Future dates show historical patterns from the previous year as estimates.
          </p>
        </div>
        <p className="mt-2 text-sm text-slate-500">Today is {todayLabel}</p>
      </header>

      <main className="max-w-5xl mx-auto px-4 pb-16 grid gap-8 lg:grid-cols-[1.1fr_1fr]">
        <EventForm onSubmit={handleSubmit} isLoading={isPending} />

        <section className="flex flex-col gap-4">
          {!data && !isPending && (
            <div className="bg-slate-900/40 rounded-xl p-6 border border-slate-800 text-slate-300">
              <h3 className="text-lg font-semibold text-white">No forecast yet</h3>
              <p className="text-sm mt-2">
                Submit the form to retrieve precipitation probability from NASA&apos;s POWER dataset. We cache results for 15
                minutes to keep the experience fast.
              </p>
            </div>
          )}
          {isError && (
            <div className="bg-rose-950/60 border border-rose-700 text-rose-100 rounded-xl p-4">
              <h4 className="font-semibold">We could not fetch your forecast.</h4>
              <p className="text-sm mt-1">{error instanceof Error ? error.message : 'Try again in a moment.'}</p>
            </div>
          )}
          {data && <ForecastResult forecast={data} />}
        </section>
      </main>

      <footer className="bg-slate-950/80 border-t border-slate-800 py-8">
        <div className="max-w-5xl mx-auto px-4 text-sm text-slate-500 space-y-2">
          <p>
            Data sources: NASA POWER (GPM IMERG), OpenStreetMap Nominatim. Built for the NASA Space Apps Challenge 2025.
          </p>
          <p>
            Designed for reliability and transparency. Check the project repository for architecture diagrams, data
            lineage, and deployment scripts.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
