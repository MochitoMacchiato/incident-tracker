from fastapi import FastAPI
from datetime import datetime, timezone
from app.models import Incident, IncidentCreate

app = FastAPI(title="Incident Tracker")

incidents: list[Incident] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/incidents", response_model=list[Incident])
def list_incidents():
    return incidents

@app.post("/incidents", response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    incident = Incident(
        id=len(incidents) + 1,
        created_at=datetime.now(timezone.utc),
        **payload.model_dump()
    )
    incidents.append(incident)
    return incident