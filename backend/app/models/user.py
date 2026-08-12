from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employ_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    lastnames = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    occupation = Column(String, nullable=True) # Área/Puesto (ej. RH, Admin)
    rest_day = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    face_img_path = Column(String, nullable=True) # <-- CORREGIDO: envuelto en Column()
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=True)
    
    schedule = relationship("Schedule", back_populates="users")
    checks = relationship("Check", back_populates="user")
    reports = relationship("Report", back_populates="user")