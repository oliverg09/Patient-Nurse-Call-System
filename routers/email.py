
import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
from db import models, database
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/export/{email}")
def export_records(email: str, db: Session = Depends(database.get_db)):
    try:
        # Obtener registros
        records = db.query(models.Records).all()
        data = [{
            'ID': record.id_record,
            'Habitación': record.room,
            'Cama': record.bed,
            'Fecha Llamada': record.patient_notice_date,
            'Fecha Aceptación': record.call_date_accepted,
            'Fecha Presencia': record.call_date_presence,
            'ID Empleado': record.id_employees
        } for record in records]
        
        df = pd.DataFrame(data)
        filename = f"historico_llamadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')

        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        
        if not sender or not password:
            raise HTTPException(status_code=500, detail="Configuración SMTP incompleta")

        # Creación del mensaje
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = email
        msg["Subject"] = "Histórico de Llamadas - NurseCare"
        msg.set_content(f"Adjunto el historico de llamadas del sistema NurseCare. Fecha: {datetime.now()}", charset='utf-8')
        msg.add_alternative("""<html><body><p>Adjunto el histórico de llamadas.</p></body></html>""", subtype="html", charset='utf-8')
        
        with open(filename, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="csv", filename=filename)

        # Conectar con SMTP
        try:
            with smtplib.SMTP_SSL("mail.gmx.com", 465, timeout=10) as servidor:
                servidor.login(sender, password)
                servidor.send_message(msg)
                logger.info(f"Correo enviado a: {email}")
        except Exception as e:
            logger.error(f"Error SMTP: {str(e)}")
        
        os.remove(filename)
        return {"status": "success", "message": f"Correo enviado a {email}"}
        
    except Exception as e:
        logger.error(f"Error general: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))