from fastapi import Request
from fastapi.responses import RedirectResponse
import json

async def auth_middleware(request: Request, call_next):
    
    # Rutas que no necesitan autenticación
    public_paths = ["/enroll", "/auth", "/static"]
    
    # Rutas que requieren ser administrador
    admin_paths = [
        "/asistentes", 
        "/asistencias",
        "/habitacion",
        "/nuevacama",
        "/crear",
        "/eliminar",
        "/modificar",
        "/crearhabitacion",
        "/crearcama",
        "/export"
    ]

    # Verifica si la ruta actual es pública
    is_public = any(request.url.path.startswith(path) for path in public_paths)
    
    if not is_public and not request.url.path == "/":
        # Verifica si existe una sesión
        session = request.cookies.get("session")
        if not session:
            return RedirectResponse(url="/enroll")
            
        try:
            # Decodifica la sesión
            session_data = json.loads(session)
            
            if not session_data.get("authenticated"):
                return RedirectResponse(url="/enroll")
            
            # Verifica permisos de administrador para rutas restringidas
            is_admin_path = any(request.url.path.startswith(path) for path in admin_paths)
            if is_admin_path and not session_data.get("is_admin"):
                return RedirectResponse(url="/panel")
                
        except:
            return RedirectResponse(url="/enroll")
    
    response = await call_next(request)
    return response