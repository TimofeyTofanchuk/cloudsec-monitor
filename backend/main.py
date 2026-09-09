from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from typing import List
from .schemas import IncidentCreate, IncidentResponse
from .alerts import send_telegram_alert

app = FastAPI(
    title="CloudSec Monitor API",
    version="1.0.0",
    description="Серверна частина системи моніторингу подій безпеки"
)

# Імітація бази збережених інцидентів (in-memory)
incidents_db: List[dict] = []

@app.get("/api/status", tags=["System"])
def get_system_status():
    return {
        "status": "online",
        "service": "CloudSec Backend Core",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/incidents", response_model=List[IncidentResponse], tags=["Incidents"])
def list_incidents():
    return incidents_db

@app.post("/api/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED, tags=["Incidents"])
def register_incident(incident: IncidentCreate):
    new_id = len(incidents_db) + 1
    record = {
        "id": new_id,
        "source_ip": incident.source_ip,
        "username": incident.username,
        "event_type": incident.event_type,
        "details": incident.details,
        "timestamp": datetime.now()
    }
    incidents_db.append(record)

    # Відправка оперативного алерту
    send_telegram_alert(
        source_ip=incident.source_ip,
        username=incident.username,
        event_type=incident.event_type,
        details=incident.details
    )
    return record
