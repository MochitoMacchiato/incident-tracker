from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Incident, Service
from .database import get_db
from .schemas import IncidentCreate, IncidentUpdate, IncidentRead

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

def get_incident_or_404(db: Session, incident_id: int) -> Incident:
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return incident

@app.post("/incidents", response_model=IncidentRead, status_code=201)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    if db.get(Service, payload.service_id) is None:
        raise HTTPException(status_code=404, detail=f"Service {payload.service_id} not found")
    incident = Incident(**payload.model_dump(mode="json"))
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@app.get("/incidents", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)):
    return db.scalars(select(Incident).order_by(Incident.id)).all()

@app.get("/incidents/{incident_id}", response_model=IncidentRead)
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    return get_incident_or_404(db, incident_id)

@app.patch("/incidents/{incident_id}", response_model=IncidentRead)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = get_incident_or_404(db, incident_id)
    changes = payload.model_dump(mode="json", exclude_unset=True)
    if "title" in changes and changes["title"] is None:
        raise HTTPException(status_code=422, detail="title cannot be null")
    for field, value in changes.items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return incident

@app.delete("/incidents/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = get_incident_or_404(db, incident_id)
    db.delete(incident)
    db.commit()