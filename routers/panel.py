from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/panel")
def panel(request: Request):
    """Página del panel principal"""
    
    return templates.TemplateResponse(
        "panel.html", 
        {"request": request}
    )