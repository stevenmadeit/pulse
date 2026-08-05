"use client";

import { useRouter } from "next/navigation";
import { resolveIncident } from "@/lib/api";

export default function ResolveIncidentButton({ incidentId }: { incidentId: string }) {
  const router = useRouter();

  return (
    <button
      type="button"
      className="rounded-3xl bg-sky-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-sky-400"
      onClick={async () => {
        await resolveIncident(incidentId);
        router.refresh();
      }}
    >
      Resolve incident
    </button>
  );
}
