from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Status(str, Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"

class IncidentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    severity: Severity
    status: Status = Status.open
    service_id: int

class IncidentUpdate (BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    severity: Severity | None = None
    status: Status | None = None

class IncidentRead (BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    severity: Severity
    status: Status
    service_id: int
    created_at: datetime   