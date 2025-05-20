from fastapi import APIRouter, Depends, HTTPException, Cookie, Request
from sqlalchemy.orm import Session
from db import models
from datetime import datetime
from db.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/aceptar/{room_number}/{bed_letter}")
def accept_call(request: Request, room_number: int, bed_letter: str, db: Session = Depends(get_db), employee_code: str | None = Cookie(default=None)):
    """Acepta la llamada y simula encender el piloto"""
   
    if not employee_code:
        raise HTTPException(status_code=401, detail="No hay sesión de empleado activa")

    # Buscar el empleado 
    employee = db.query(models.Employee).filter(
        models.Employee.code_employees == employee_code
    ).first()

    if not employee:
        raise HTTPException(status_code=401, detail="Empleado no encontrado")

    # Buscar la cama
    bed = db.query(models.Beds).join(models.Room).filter(
        models.Room.room_number == room_number,
        models.Beds.bed_letter == bed_letter
    ).first()

    if not bed:
        raise HTTPException(status_code=404, detail="Cama no encontrada")

    # Buscar el registro de llamada pendiente
    record = db.query(models.Records).filter(
        models.Records.room == room_number,
        models.Records.bed == bed_letter,
        models.Records.call_date_accepted == None
    ).order_by(models.Records.patient_notice_date.desc()).first()
    
    if not record:
        return templates.TemplateResponse(
            "accept_panel.html",
            {"request": request, "room": room_number, "bed": bed_letter, "error": True, "message": "La solicitud ha sido aceptada por otro asistente"}
        )

    # Registrar la aceptación y el empleado que la acepta
    record.call_date_accepted = datetime.now()
    record.id_employees = employee.dni_employees
    db.commit()

    return templates.TemplateResponse(
        "accept_panel.html",
        {"request": request, "room": room_number, "bed": bed_letter, "error": False, "message": "Llamada aceptada correctamente"}
    )