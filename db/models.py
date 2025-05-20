from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Room(Base):
    __tablename__ = "room"
    id_room = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_number = Column(Integer, unique=True)
    beds = relationship("Beds", back_populates="room")

class Beds(Base):
    __tablename__ = "beds"
    id_bed = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip_bed = Column(String(50), unique=True)
    bed_letter = Column(String(1))  # 'a' o 'b'
    id_room = Column(Integer, ForeignKey("room.id_room"))
    room = relationship("Room", back_populates="beds")
    
    # No puede haber dos camas con la misma letra en la misma habitación
    __table_args__ = (UniqueConstraint('bed_letter', 'id_room', name='uq_bed_letter_room'),)

class Employee(Base):
    __tablename__ = "employees"
    dni_employees = Column(String(10), primary_key=True)
    name_employees = Column(String(50))
    code_employees = Column(String(6), unique=True)
    admin = Column(Boolean) 
    records = relationship("Records", back_populates="employee")

class Records(Base):
    __tablename__ = "record"
    id_record = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room = Column(Integer)
    bed = Column(String(1)) 
    call_date_accepted = Column(DateTime)
    call_date_presence = Column(DateTime)
    patient_notice_date = Column(DateTime)
    id_employees = Column(Integer, ForeignKey("employees.dni_employees"))
    employee = relationship("Employee", back_populates="records")