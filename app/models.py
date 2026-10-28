from pydantic import BaseModel, Field
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = ""

class Incident(IncidentCreate):
    id: int
    created_at : datetime