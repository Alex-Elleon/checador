from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    check_in = Column(String, nullable=False)   # Ej: "08:00"
    check_out = Column(String, nullable=False)  # Ej: "16:00"
    date = Column(String, nullable=True)
    worked_days = Column(String, nullable=True) # Ej: "L,M,M,J,V"
    late_minutes = Column(Integer, default=15)  # Tolerancia en minutos

    users = relationship("User", back_populates="schedule")