from fastapi import FastAPI, HTTPException
from typing import List

from ingestion.database import get_session, Incident

app = FastAPI(title="Pulse Data Quality API")


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
        return {
            "id": incident.id,
            "source": incident.source,
            "check_type": incident.check_type,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "created_at": incident.created_at.isoformat(),
            "ai_summary": incident.ai_summary,
            "resolved_at": incident.resolved_at.isoformat() if incident.resolved_at else None,
        }
    finally:
        session.close()
