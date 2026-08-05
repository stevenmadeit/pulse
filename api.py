import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text

from ingestion.database import get_session, Incident, RawIngestRun

app = FastAPI(title="Pulse Data Quality API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ingest_runs")
def list_ingest_runs(limit: int = 10):
    session = get_session()
    try:
        runs = session.execute(
            select(RawIngestRun).order_by(RawIngestRun.run_at.desc()).limit(limit)
        ).scalars().all()
        return [
            {
                "id": run.id,
                "source": run.source,
                "record_count": run.record_count,
                "run_at": run.run_at.isoformat(),
            }
            for run in runs
        ]
    finally:
        session.close()


@app.get("/snapshot")
def get_snapshot():
    session = get_session()
    try:
        def one(query):
            row = session.execute(text(query)).mappings().first()
            return dict(row) if row else None

        def many(query):
            return [dict(row) for row in session.execute(text(query)).mappings().all()]

        weather = one(
            "SELECT city, temperature, condition, ingested_at FROM stg_weather ORDER BY ingested_at DESC LIMIT 1"
        )
        sports = one(
            "SELECT home_team, away_team, home_score, away_score, game_date, ingested_at FROM stg_sports ORDER BY game_date DESC LIMIT 1"
        )
        crypto = many(
            "SELECT coin, price_usd, ingested_at FROM stg_crypto ORDER BY ingested_at DESC LIMIT 5"
        )
        return {"weather": weather, "sports": sports, "crypto": crypto}
    except Exception:
        return {"weather": None, "sports": None, "crypto": []}
    finally:
        session.close()


@app.get("/incidents")
def list_incidents():
    session = get_session()
    try:
        incidents = session.query(Incident).order_by(Incident.created_at.desc()).all()
        result = [
            {
                "id": i.id,
                "source": i.source,
                "check_type": i.check_type,
                "description": i.description,
                "severity": i.severity,
                "status": i.status,
                "created_at": i.created_at.isoformat(),
                "ai_summary": i.ai_summary,
                "resolved_at": i.resolved_at.isoformat() if i.resolved_at else None,
            }
            for i in incidents
        ]
        return result
    finally:
        session.close()


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    session = get_session()
    try:
        incident = session.query(Incident).filter(Incident.id == incident_id).one_or_none()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        ai_summary = None
        if incident.ai_summary:
            try:
                ai_summary = json.loads(incident.ai_summary)
            except Exception:
                ai_summary = {"raw": incident.ai_summary}

        return {
            "id": incident.id,
            "source": incident.source,
            "check_type": incident.check_type,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "created_at": incident.created_at.isoformat(),
            "ai_summary": ai_summary,
            "resolved_at": incident.resolved_at.isoformat() if incident.resolved_at else None,
        }
    finally:
        session.close()


@app.post("/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: int):
    session = get_session()
    try:
        incident = session.query(Incident).filter(Incident.id == incident_id).one_or_none()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        incident.status = "resolved"
        incident.resolved_at = incident.resolved_at or __import__("datetime").datetime.utcnow()
        session.commit()
        return {"id": incident.id, "status": incident.status, "resolved_at": incident.resolved_at.isoformat()}
    finally:
        session.close()
