export const API_BASE = "http://127.0.0.1:8000";

export async function fetchIncidents() {
  const res = await fetch(`${API_BASE}/incidents`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load incidents");
  return res.json();
}

export async function fetchIncident(id: string) {
  const res = await fetch(`${API_BASE}/incidents/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load incident");
  return res.json();
}

export async function fetchIngestRuns() {
  const res = await fetch(`${API_BASE}/ingest_runs`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load ingest runs");
  return res.json();
}

export async function fetchSnapshot() {
  const res = await fetch(`${API_BASE}/snapshot`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load snapshot");
  return res.json();
}

export async function resolveIncident(id: string) {
  const res = await fetch(`${API_BASE}/incidents/${id}/resolve`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to resolve incident");
  return res.json();
}
