from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db import models
from datetime import datetime, timedelta
from db.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/asistencias")
def get_attendance(request: Request, db: Session = Depends(get_db)):
    """Obtiene asistencias pendientes y realizadas en las últimas 24 horas"""

    now = datetime.now()
    last_24h = now - timedelta(hours=24)

    # Asistencias realizadas
    made = db.query(models.Records).filter(
        models.Records.call_date_accepted >= last_24h
    ).all()

    # Asistencias pendientes
    pending = db.query(models.Records).filter(
        and_(
            models.Records.patient_notice_date >= last_24h,
            models.Records.call_date_accepted == None
        )
    ).all()

    if not made and not pending:
        return templates.TemplateResponse(
            "attendance_panel.html",
            {"request": request, "attendance": {"made": [], "pending": []}, "error_message": "No se encontraron asistencias en las últimas 24 horas"}
        )

    attendance_data = {
        "made": [{"room": record.room, "bed": record.bed, "patient_notice_date": record.patient_notice_date, "call_date_accepted": record.call_date_accepted, "id_employees":record.id_employees} for record in made],
        "pending": [{"room": record.room, "bed": record.bed, "patient_notice_date": record.patient_notice_date} for record in pending]
    }

    return templates.TemplateResponse(
        "attendance_panel.html",
        {"request": request, "attendance": attendance_data}
    )
