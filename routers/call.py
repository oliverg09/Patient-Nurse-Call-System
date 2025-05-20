from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models
from datetime import datetime
from notifications import send_pushover_message  
from db.database import get_db

router = APIRouter()  

@router.get("/llamada/{room_number}/{bed_letter}")
def call_registration(room_number: int, bed_letter: str, db: Session = Depends(get_db)):
    """Registrar llamada de asistencia en la cama especificada"""
    
    # ¿Existe la cama?
    bed1 = db.query(models.Beds).filter(
        models.Beds.bed_letter == f"{bed_letter}"
    ).first()

    # ¿Existe la habitación?
    room1 = db.query(models.Room).filter(
        models.Room.room_number == f"{room_number}",
    ).first()
    
    if not bed1:
        raise HTTPException(status_code=404, detail="Cama no encontrada")
    
    if not room1:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")
    
    url = f"http://127.0.0.1:8000/aceptar/{room_number}/{bed_letter}"  
    
    # Registro llamada en base de datos 'api_nursing-patient'
    new_registration = models.Records(
        room=room_number,
        bed=bed_letter,
        patient_notice_date=datetime.now(),
        id_employees=None # Aún no se conoce el empleado
    )
    
    db.add(new_registration)
    db.commit()

    mensaje = f"Solicitud de asistencia en habitación <b><font color='red'>{room_number}</font></b> y cama <b><font color='red'>{bed_letter}</font></b>"
    send_pushover_message("ASISTENCIA", mensaje, url)

    return {"status": "ok", "mensaje": "Llamada registrada y notificada"}

@router.get("/verificarestado/{room_number}/{bed_letter}")
def check_lamp_status(room_number: int, bed_letter: str, db: Session = Depends(get_db)):
    """Verificar el estado de la lámpara"""
    
    # Buscar el registro más reciente para esta habitación y cama
    record = db.query(models.Records).filter(
        models.Records.room == room_number,
        models.Records.bed == bed_letter,
        models.Records.call_date_presence == None  # No ha llegado el enfermero 
    ).order_by(models.Records.patient_notice_date.desc()).first()
    
    if not record:
        return {"lamp_state": "off"}
        
    # Si hay un registro y tiene fecha de aceptación pero no de presencia
    if record.call_date_accepted and not record.call_date_presence:
        return {"lamp_state": "on"}
        
    return {"lamp_state": "off"}

