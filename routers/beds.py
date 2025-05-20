from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import models, database

from db.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/camas")
def get_beds(request: Request, db: Session = Depends(get_db)):
    """Obtener todas las habitaciones con sus camas correspondientes"""
    
    # Obtener todas las habitaciones
    rooms = db.query(models.Room).all()
    
    if not rooms:
        return templates.TemplateResponse(
            "beds_panel.html",
            {"request": request, "rooms": [], "error_message": "No se encontraron habitaciones en el sistema"}
        )
    
    room_data = []
    for room in rooms:
        # Obtener las camas de esta habitación
        beds = db.query(models.Beds).filter(models.Beds.id_room == room.id_room).all()
        
        bed_list = []
        for bed in beds:
            bed_list.append({
                "id_bed": bed.id_bed,
                "bed_letter": bed.bed_letter, 
                "room": room.room_number,
                "display_name": f"Habitación {room.room_number} - Cama {bed.bed_letter}"
            })

        # Añadir la habitación con sus camas al resultado
        room_data.append({
            "room_number": room.room_number,
            "beds": bed_list
        })
    
    if not room_data or all(len(room["beds"]) == 0 for room in room_data):
        return templates.TemplateResponse(
            "beds_panel.html",
            {"request": request, "rooms": [], "error_message": "No hay camas disponibles en el sistema"}
        )
    
    return templates.TemplateResponse(
        "beds_panel.html",
        {"request": request, "rooms": room_data}
    )