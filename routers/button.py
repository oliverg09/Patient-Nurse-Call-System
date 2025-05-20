from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/pulsador/{room}/{bed_letter}")
def button(request: Request, room: str, bed_letter: str):
    """Página del pulsador"""
    
    return templates.TemplateResponse(
        "room_panel.html", 
        {"request": request, "room": room, "bed": bed_letter}
    )