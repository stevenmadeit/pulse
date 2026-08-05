import Link from "next/link";
import { fetchIncident } from "@/lib/api";
import ResolveIncidentButton from "@/components/ResolveIncidentButton";

interface IncidentPageProps {
  params: { id: string };
}

const severityClasses: Record<string, string> = {
  high: "bg-rose-600 text-white",
  medium: "bg-amber-500 text-slate-950",
  low: "bg-emerald-500 text-slate-950",
  resolved: "bg-slate-600 text-slate-100",
};

function statusLabel(status: string, severity: string) {
  const classes = severityClasses[severity] ?? "bg-slate-700 text-slate-100";
  return <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] ${classes}`}>{status}</span>;
}

export default async function IncidentDetail({ params }: IncidentPageProps) {
  const incident = await fetchIncident(params.id);

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-slate-100">
      <div className="mx-auto max-w-5xl space-y-6">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/20">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.28em] text-sky-400/80">Incident Detail</p>
              <h1 className="mt-2 text-3xl font-semibold text-white">#{incident.id} • {incident.source}</h1>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {statusLabel(incident.status, incident.severity)}
              <Link href="/" className="rounded-full border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-100 transition hover:border-slate-500 hover:bg-slate-700">
                Back to dashboard
              </Link>
            </div>
          </div>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div className="rounded-3xl bg-slate-950/80 p-4">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Check type</p>
              <p className="mt-2 text-lg font-semibold text-white">{incident.check_type}</p>
            </div>
            <div className="rounded-3xl bg-slate-950/80 p-4">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Created</p>
              <p className="mt-2 text-lg font-semibold text-white">{new Date(incident.created_at).toLocaleString()}</p>
            </div>
          </div>
          <div className="mt-6 rounded-3xl bg-slate-950/80 p-4">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Description</p>
            <p className="mt-2 text-base text-slate-200">{incident.description}</p>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl bg-slate-950/80 p-4">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Source</p>
              <p className="mt-2 text-lg font-semibold text-white">{incident.source}</p>
            </div>
            <div className="rounded-3xl bg-slate-950/80 p-4">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Severity</p>
              <p className="mt-2 text-lg font-semibold text-white">{incident.severity}</p>
            </div>
            <div className="rounded-3xl bg-slate-950/80 p-4">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Status</p>
              <p className="mt-2 text-lg font-semibold text-white">{incident.status}</p>
            </div>
          </div>
          <div className="mt-6 space-y-4">
            <div className="rounded-3xl bg-slate-950/80 p-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">AI investigation</p>
              {incident.ai_summary ? (
                <div className="mt-4 space-y-4 text-slate-200">
                  <div>
                    <p className="text-sm font-semibold text-white">Likely cause</p>
                    <p className="mt-2 text-sm text-slate-300">{incident.ai_summary.likely_cause || incident.ai_summary.raw || "No details"}</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">Impact</p>
                    <p className="mt-2 text-sm text-slate-300">{incident.ai_summary.impact || "No details"}</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">Suggested fix</p>
                    <p className="mt-2 text-sm text-slate-300">{incident.ai_summary.suggested_fix || "No details"}</p>
                  </div>
                </div>
              ) : (
                <p className="mt-4 text-sm text-slate-500">AI summary not available for this incident.</p>
              )}
            </div>
          </div>
          <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <ResolveIncidentButton incidentId={params.id} />
            {incident.resolved_at && (
              <p className="text-sm text-slate-400">Resolved at {new Date(incident.resolved_at).toLocaleString()}</p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
