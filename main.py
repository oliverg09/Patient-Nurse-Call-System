from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import models, database

from routers.call import router as call_router  
from routers.presence import router as presence_router  
from routers.accept import router as accept_router 
from routers.employees import router as employees_router 
from routers.attendance import router as attendance_router 
from routers.beds import router as beds_router 
from routers.button import router as button_router
from routers.panel import router as panel_router
from routers.create_beds import router as create_beds_router
from routers.create_room import router as create_rooms_router
from routers.login import router as login_router
from routers.email import router as email_router
from middleware.auth import auth_middleware

app = FastAPI()

# Todo lo que esté en la carpeta "static" será accesible desde el navegador en /static/...
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=database.engine)

app.include_router(call_router)
app.include_router(presence_router)
app.include_router(accept_router)
app.include_router(employees_router)
app.include_router(attendance_router)
app.include_router(beds_router)
app.include_router(button_router)
app.include_router(panel_router)
app.include_router(create_beds_router)
app.include_router(create_rooms_router)
app.include_router(login_router)
app.include_router(email_router)
app.middleware("http")(auth_middleware)
