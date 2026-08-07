const DEFAULT_API_BASE = "http://127.0.0.1:8000";
export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || DEFAULT_API_BASE;

async function requestJson(path: string, init?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    ...init,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Request failed (${res.status}): ${text || res.statusText}`);
  }

  return res.json();
}

export async function fetchIncidents() {
  return requestJson("/incidents");
}

export async function fetchIncident(id: string) {
  return requestJson(`/incidents/${id}`);
}

export async function fetchIngestRuns() {
  return requestJson("/ingest_runs");
}

export async function fetchSnapshot() {
  return requestJson("/snapshot");
}

export async function resolveIncident(id: string) {
  return requestJson(`/incidents/${id}/resolve`, { method: "POST" });
}
