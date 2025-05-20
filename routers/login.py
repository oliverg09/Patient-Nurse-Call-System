from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
import json

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/enroll")
def enroll(request: Request):
    """Página login"""

    return templates.TemplateResponse(
        "login_panel.html", 
        {"request": request}
    )

@router.get("/desenroll")
def desenroll(response: Response):
    """Cerrar sesión"""

    response.delete_cookie(key="session")
    response.delete_cookie(key="employee_code")
    return {"status": "logged_out"}

@router.get("/auth/{username}/{password}")
def authenticate(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    """Autenticar usuario"""

    # Convertir password a string para comparar
    password = str(password)
    
    employee = db.query(models.Employee).filter(
        models.Employee.name_employees == username,
        models.Employee.code_employees == password
    ).first()
    
    if not employee:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Establecer cookies de sesión con los datos correctos
    session_data = {
        "authenticated": True,
        "is_admin": bool(employee.admin),  
        "username": employee.name_employees
    }
    
    # Guarda sesion (si está autenticado, si es admin, su nombre)
    response.set_cookie(
        key="session",
        value=json.dumps(session_data),
        httponly=True,
        max_age=28800  # 8 horas
    )

    response.set_cookie(
        key="employee_code", 
        value=str(employee.code_employees),
        httponly=True,
        max_age=28800
    )
    
    # Devolver la respuesta 
    return {"status": "success", "authenticated": True, "is_admin": bool(employee.admin), "username": employee.name_employees}