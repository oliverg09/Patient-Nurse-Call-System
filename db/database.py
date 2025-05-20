from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# pip install python-dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener variables de entorno
USUARIO = os.getenv("MYSQL_USER")
CONTRASENA = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PUERTO = os.getenv("MYSQL_PORT")
BD = os.getenv("MYSQL_DB")

DATABASE_URL = f"mysql+pymysql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BD}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()