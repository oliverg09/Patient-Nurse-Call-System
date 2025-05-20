from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/habitacion")
def rooms(request: Request):
    return templates.TemplateResponse(
        "create_rooms.html", 
        {"request": request}
    )

@router.get("/crearhabitacion/{room}")
def createrooms(request: Request, room: str, db: Session = Depends(get_db)):
    """Crear una nueva habitacion"""

    new_room = models.Room(
        room_number=room
    )
        
    db.add(new_room)
    db.commit()
    
    return templates.TemplateResponse(
        "create_rooms.html", 
        {"request": request}
    )
