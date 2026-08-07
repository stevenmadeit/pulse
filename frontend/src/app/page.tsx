import Link from "next/link";
import { fetchIncidents, fetchIngestRuns, fetchSnapshot } from "@/lib/api";

const severityClasses: Record<string, string> = {
  high: "bg-rose-600 text-white",
  medium: "bg-amber-500 text-slate-950",
  low: "bg-emerald-500 text-slate-950",
  resolved: "bg-slate-600 text-slate-100",
};

const statusClasses: Record<string, string> = {
  resolved: "bg-emerald-600 text-slate-950",
  open: "bg-amber-500 text-slate-950",
};

function badge(value: string) {
  const classes = severityClasses[value] ?? statusClasses[value] ?? "bg-slate-700 text-slate-100";
  return <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] ${classes}`}>{value}</span>;
}

export default async function Home() {
  const incidents = await fetchIncidents();
  const ingestRuns = await fetchIngestRuns();
  const snapshot = await fetchSnapshot();

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-slate-100">
      <div className="mx-auto flex max-w-7xl flex-col gap-8">
        <header className="flex flex-col gap-3 rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/20 backdrop-blur">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.28em] text-sky-400/80">Pulse</p>
              <h1 className="text-4xl font-semibold text-white">Data Quality Dashboard</h1>
            </div>
            <div className="grid gap-2 sm:auto-cols-fr sm:grid-flow-col">
              <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Incident Count</p>
                <p className="mt-2 text-3xl font-semibold text-white">{incidents.length}</p>
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Latest Run</p>
                <p className="mt-2 text-3xl font-semibold text-white">{ingestRuns[0]?.source ?? "n/a"}</p>
              </div>
            </div>
          </div>
          <p className="max-w-2xl text-slate-400">Monitor ingestion history, incidents, and the latest transformed snapshot in one place.</p>
        </header>

        <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
          <div className="space-y-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/20">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold text-white">Pipeline run history</h2>
                <p className="text-sm text-slate-400">Most recent ingestion events by source</p>
              </div>
            </div>
            <div className="grid gap-4">
              {ingestRuns.map((run: any) => (
                <div key={run.id} className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4 sm:flex sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">{run.source}</p>
                    <p className="mt-2 text-lg font-semibold text-white">{run.record_count} rows</p>
                  </div>
                  <p className="mt-4 text-sm text-slate-400 sm:mt-0">{new Date(run.run_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/20">
            <div>
              <h2 className="text-xl font-semibold text-white">Latest snapshot</h2>
              <p className="text-sm text-slate-400">Weather, sports, and crypto from transformed tables</p>
            </div>
            <div className="grid gap-4">
              <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
                <h3 className="text-sm uppercase tracking-[0.24em] text-slate-500">Weather</h3>
                {snapshot.weather ? (
                  <div className="mt-3 space-y-1 text-sm text-slate-200">
                    <p className="font-semibold text-white">{snapshot.weather.city}</p>
                    <p>{snapshot.weather.temperature}°C • {snapshot.weather.condition}</p>
                    <p className="text-slate-500">Updated {new Date(snapshot.weather.ingested_at).toLocaleString()}</p>
                  </div>
                ) : (
                  <p className="mt-3 text-slate-500">No weather snapshot available</p>
                )}
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
                <h3 className="text-sm uppercase tracking-[0.24em] text-slate-500">Sports</h3>
                {snapshot.sports ? (
                  <div className="mt-3 space-y-1 text-sm text-slate-200">
                    <p className="font-semibold text-white">{snapshot.sports.home_team} vs {snapshot.sports.away_team}</p>
                    <p>{snapshot.sports.home_score} - {snapshot.sports.away_score}</p>
                    <p className="text-slate-500">Game date {new Date(snapshot.sports.game_date).toLocaleString()}</p>
                  </div>
                ) : (
                  <p className="mt-3 text-slate-500">No sports snapshot available</p>
                )}
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
                <h3 className="text-sm uppercase tracking-[0.24em] text-slate-500">Crypto</h3>
                {snapshot.crypto.length ? (
                  <div className="mt-3 grid gap-2 text-sm text-slate-200">
                    {snapshot.crypto.map((coin: any) => (
                      <div key={coin.coin} className="flex items-center justify-between gap-2 rounded-2xl bg-slate-900/70 px-3 py-2">
                        <span>{coin.coin}</span>
                        <span className="font-semibold text-white">${coin.price_usd.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="mt-3 text-slate-500">No crypto snapshot available</p>
                )}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/20">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-white">Data quality incidents</h2>
              <p className="text-sm text-slate-400">Sorted most recent first</p>
            </div>
            <Link href="/" className="rounded-full bg-slate-800 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700">Refresh</Link>
          </div>
          <div className="mt-6 space-y-3">
            {incidents.map((incident: any) => (
              <Link
                key={incident.id}
                href={`/incidents/${incident.id}`}
                className="block rounded-3xl border border-slate-800 bg-slate-950/80 p-4 transition hover:border-slate-600"
              >
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">{incident.source} • {incident.check_type}</p>
                    <p className="mt-2 text-lg font-semibold text-white">{incident.description}</p>
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    {badge(incident.severity)}
                    {badge(incident.status)}
                  </div>
                </div>
                <p className="mt-4 text-sm text-slate-400">Created {new Date(incident.created_at).toLocaleString()}</p>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
