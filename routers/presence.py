from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models
from datetime import datetime
from db.database import get_db

router = APIRouter()

@router.get("/presencia/{room_number}/{bed_letter}")
def register_presence(room_number: int, bed_letter: str, db: Session = Depends(get_db)):
    """Registrar presencia y apagar el piloto"""
    
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
        models.Records.call_date_presence == None
    ).order_by(models.Records.call_date_accepted.desc()).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="No hay llamadas pendientes para esta cama")

    record.call_date_presence = datetime.now()
    db.commit()

    return {"status": "ok", "lamp_state": "off"}