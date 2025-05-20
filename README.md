# NurseCare - Sistema de Llamadas Paciente-Enfermero

## Descripción
Sistema web para gestionar llamadas de asistencia entre pacientes y personal de enfermería en un entorno hospitalario.

## Tecnologías Utilizadas

### Backend
- Python 3.x
- FastAPI (Framework web)
- SQLAlchemy (ORM)
- MySQL (Base de datos)
- Jinja2 (Motor de plantillas)

### Frontend 
- HTML5
- CSS3
- JavaScript
- Diseño responsive

### Integraciones
- Pushover API (Notificaciones)
- SMTP (Envío de emails)

### Herramientas de Desarrollo
- Visual Studio Code
- Git/GitHub
- Nginx (Servidor web)

## Estructura de Base de Datos

### Tablas Principales
- `room` - Habitaciones
- `beds` - Camas 
- `employees` - Personal de enfermería
- `records` - Registro de llamadas/asistencias

## Funcionalidades Principales

- Gestión de usuarios (CRUD)
- Registro de llamadas de asistencia
- Notificaciones en tiempo real
- Seguimiento de asistencias
- Panel de administración
- Exportación de históricos
- Sistema de autenticación
- Roles de usuario (Admin/Normal)

## Configuración

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno (.env):
```
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=
MYSQL_PORT=
MYSQL_DB=

EMAIL_USER=
EMAIL_PASSWORD=

PUSHOVER_USER_KEY=
PUSHOVER_API_TOKEN=
```

3. Crear base de datos MySQL

4. Iniciar servidor:
```bash
uvicorn main:app --reload
```

## Estructura del Proyecto
```
├── main.py
├── db/
│   ├── database.py
│   └── models.py
├── routers/
│   ├── accept.py
│   ├── attendance.py
│   ├── beds.py
│   └── ...
├── html/
├── static/
└── middleware/
```

## Seguridad
- Autenticación mediante cookies
- Middleware de autorización
- Protección de rutas admin
- Encriptación de contraseñas

## Autor
Oliver Garcia González
