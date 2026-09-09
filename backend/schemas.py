from pydantic import BaseModel, Field
from datetime import datetime

class IncidentCreate(BaseModel):
    source_ip: str = Field(..., description="IP-адреса джерела атаки")
    username: str = Field(..., description="Цільовий обліковий запис")
    event_type: str = Field(..., description="Тип події, наприклад: SSH_BRUTEFORCE")
    details: str = Field(..., description="Детальний опис події")

class IncidentResponse(IncidentCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
