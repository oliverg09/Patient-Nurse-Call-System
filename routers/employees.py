from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/asistentes")
def get_employees(request: Request, db: Session = Depends(get_db)):
    """Obtener todos los asistentes"""
    
    employees = db.query(models.Employee).all()
    
    return templates.TemplateResponse(
        "CRUD_employees.html", 
        {"request": request, "employees": employees}
    )

@router.get("/crear/{name}/{password}/{dni}/{admin}")
def create_employee(request: Request, name: str, password: str, dni:str, admin:int, db: Session = Depends(get_db)):
    """Crear un nuevo empleado"""
    
    # Validaciones básicas
    if not name or not name.strip():
        return {"error": "El nombre del empleado no puede estar vacío"}

    if not password or not password.strip():
        return {"error": "La contraseña no puede estar vacía"}

    try:
        # Verificar si el empleado ya existe
        existing_employee = db.query(models.Employee).filter(
            models.Employee.dni_employees == dni
        ).first()
        
        if existing_employee:
            return {"error": "Ya existe un empleado con ese DNI"}
            
        # Crear nuevo empleado
        new_employee = models.Employee(
            name_employees=name,
            code_employees=password,
            dni_employees=dni,
            admin = admin
        )
        
        db.add(new_employee)
        db.commit()
        
        return {"success": "Usuario creado correctamente"}
        
    except Exception as e:
        db.rollback()
        return {"error": "Error al crear el empleado"}
    
@router.get("/eliminar/{dni}")
def delete_employee(request: Request, dni: str, db: Session = Depends(get_db)):
    """Eliminar un empleado"""
    
    try:
        # Verificar si el empleado existe
        delete_employee = db.query(models.Employee).filter(
            models.Employee.dni_employees == dni
        ).first()
        
        if not delete_employee:
            return {"error": "Empleado no encontrado"}
        
        # Eliminar el empleado
        db.delete(delete_employee)
        db.commit()
        
        return {"success": "Empleado eliminado correctamente"}
        
    except Exception as e:
        db.rollback()
        return {"error": "Error al eliminar el empleado"}

@router.get("/modificar/{dni}/{name}/{password}/{admin}")
def update_employee(request: Request, dni: str, name: str, password: str, admin:int, db: Session = Depends(get_db)):
    """Actualizar un empleado"""
    
    try:
        # Verificar si el empleado existe
        update_employee = db.query(models.Employee).filter(
            models.Employee.dni_employees == dni
        ).first()
        
        if not update_employee:
            return {"error": "Empleado no encontrado"}
        
        # Actualizar el empleado
        if name == "":
            name = update_employee.name_employees
        update_employee.name_employees = name

        if password == "":
            password = update_employee.code_employees
        update_employee.code_employees = password
        
        if dni == "":
            dni = update_employee.dni_employees
        update_employee.dni_employees = dni

        update_employee.admin = admin
        
        db.commit()
        
        return {"success": "Empleado actualizado correctamente"}
        
    except Exception as e:
        db.rollback()
        return {"error": "Error al actualizar el empleado"}