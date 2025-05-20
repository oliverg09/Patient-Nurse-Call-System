
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/nuevacama")
def beds(request: Request, db: Session = Depends(get_db)):
    """Obtener todos las habitaciones"""

    rooms = db.query(models.Room).all()
    
    return templates.TemplateResponse(
        "create_beds.html", 
        {"request": request, "rooms": rooms}
    )

@router.get("/crearcama/{room}/{bed}/{ip}")
def createbed(request: Request, room: str, bed: str, ip: str, db: Session = Depends(get_db)):
    """Crear una nueva cama"""
    
    # Verificamos si ya existe una cama con la misma letra en la habitación
    existing_bed = db.query(models.Beds).filter(
        models.Beds.id_room == room,
        models.Beds.bed_letter == bed
    ).first()
    
    if existing_bed:
        return JSONResponse(
            status_code=400,
            content={"error": "Ya existe una cama igual"}
        )
    
    # Verificamos si la IP ya está en uso
    existing_ip = db.query(models.Beds).filter(
        models.Beds.ip_bed == ip
    ).first()
    
    if existing_ip:
        return JSONResponse(
            status_code=400,
            content={"error": "La IP ya está asignada a otra cama"}
        )
    
    try:
        new_bed = models.Beds(
            id_room=room,
            bed_letter=bed,
            ip_bed = ip
        )
            
        db.add(new_bed)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"message": "Cama creada exitosamente"}
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": "Error al crear la cama"}
        )