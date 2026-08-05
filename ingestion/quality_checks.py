import json
from sqlalchemy import select

from ingestion.ai_investigator import generate_ai_summary
from ingestion.database import (
    RawWeather,
    RawSports,
    RawCrypto,
    RawIngestRun,
    create_incident,
)


SOURCE_MODEL = {
    "weather": RawWeather,
    "sports": RawSports,
    "crypto": RawCrypto,
}


def _get_latest_runs(session, source):
    stmt = select(RawIngestRun).where(RawIngestRun.source == source).order_by(RawIngestRun.run_at.desc()).limit(2)
    return session.execute(stmt).scalars().all()


def _get_latest_raw_records(session, source, limit=10):
    model = SOURCE_MODEL[source]
    stmt = select(model).order_by(model.ingested_at.desc()).limit(limit)
    return session.execute(stmt).scalars().all()


def _build_ai_summary_text(ai_summary: dict | None) -> str | None:
    if not ai_summary:
        return None
    return json.dumps(ai_summary, ensure_ascii=False)


def run_checks_for_source(session, source: str):
    incidents = []
    # Row count drop check
    runs = _get_latest_runs(session, source)
    if len(runs) >= 2:
        latest, prev = runs[0], runs[1]
        if prev.record_count and latest.record_count < prev.record_count * 0.5:
            drop_pct = 100.0 * (1 - (latest.record_count / prev.record_count))
            severity = "high" if drop_pct > 90 else "medium"
            desc = f"Row count dropped by {drop_pct:.1f}% (from {prev.record_count} to {latest.record_count})"
            ai_summary = generate_ai_summary("row_count_drop", source, desc, severity, {"previous_count": prev.record_count, "latest_count": latest.record_count})
            inc = create_incident(session, source, "row_count_drop", desc, severity, _build_ai_summary_text(ai_summary))
            incidents.append(inc)

    # Unexpected nulls and schema changes & duplicates
    records = _get_latest_raw_records(session, source, limit=5)
    if records:
        latest = records[0]
        try:
            payload = json.loads(latest.raw_json)
        except Exception:
            payload = {}

        # Schema check: compare keys to previous record
        if len(records) >= 2:
            try:
                prev_payload = json.loads(records[1].raw_json)
            except Exception:
                prev_payload = {}
            latest_keys = set(payload.keys())
            prev_keys = set(prev_payload.keys())
            added = latest_keys - prev_keys
            removed = prev_keys - latest_keys
            if added or removed:
                desc = f"Schema change detected. Added: {list(added)}, Removed: {list(removed)}"
                ai_summary = generate_ai_summary("schema_change", source, desc, "medium", {"added_keys": list(added), "removed_keys": list(removed)})
                inc = create_incident(session, source, "schema_change", desc, "medium", _build_ai_summary_text(ai_summary))
                incidents.append(inc)

        # Null checks per source
        if source == "weather":
            temp = None
            cw = payload.get("current_weather") or {}
            temp = cw.get("temperature") if isinstance(cw, dict) else None
            if temp is None:
                desc = "Missing temperature in latest weather payload"
                ai_summary = generate_ai_summary("missing_temperature", source, desc, "high", {"payload": payload})
                inc = create_incident(session, source, "missing_temperature", desc, "high", _build_ai_summary_text(ai_summary))
                incidents.append(inc)

        if source == "crypto":
            # payload is a mapping of coin->{usd: value}
            missing = []
            for coin, data in (payload.items() if isinstance(payload, dict) else []):
                if not data or (isinstance(data, dict) and data.get("usd") is None):
                    missing.append(coin)
            if missing:
                desc = f"Missing price for coins: {missing} in latest crypto payload"
                ai_summary = generate_ai_summary("missing_prices", source, desc, "high", {"payload": payload})
                inc = create_incident(session, source, "missing_prices", desc, "high", _build_ai_summary_text(ai_summary))
                incidents.append(inc)

        if source == "sports":
            # Expect events list with scores in entries
            events = payload.get("events") if isinstance(payload, dict) else None
            if events is None:
                desc = "Missing events in sports payload"
                inc = create_incident(session, source, "missing_events", desc, "high")
                incidents.append(inc)
            else:
                # check for missing scores
                for ev in events:
                    competitions = ev.get("competitions") if isinstance(ev, dict) else None
                    if competitions:
                        for comp in competitions:
                            if comp.get("competitors"):
                                for c in comp.get("competitors"):
                                    if c.get("score") is None:
                                        desc = f"Missing score in event {ev.get('id')} competitor {c.get('id')}"
                                        ai_summary = generate_ai_summary("missing_scores", source, desc, "medium", {"payload": payload})
                                        inc = create_incident(session, source, "missing_scores", desc, "medium", _build_ai_summary_text(ai_summary))
                                        incidents.append(inc)

        # Duplicate detection in recent records (exact raw_json match)
        raw_texts = [r.raw_json for r in records]
        dupcounts = {}
        for rt in raw_texts:
            dupcounts[rt] = dupcounts.get(rt, 0) + 1
        for rt, cnt in dupcounts.items():
            if cnt > 1:
                desc = f"Found {cnt} duplicate raw records in recent ingestion for {source}"
                ai_summary = generate_ai_summary("duplicates", source, desc, "low", {"payload": payload})
                inc = create_incident(session, source, "duplicates", desc, "low", _build_ai_summary_text(ai_summary))
                incidents.append(inc)

    return incidents


def run_all_checks(session):
    results = {}
    for src in ["weather", "sports", "crypto"]:
        results[src] = run_checks_for_source(session, src)
    return results
