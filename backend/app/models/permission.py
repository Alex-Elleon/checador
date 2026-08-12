from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # "VACACIONES", "PERMISO", "INCAPACIDAD"
    date = Column(String)  # "2026-08-12"
    reason = Column(String)
    status = Column(String, default="APROBADO")  # "PENDIENTE", "APROBADO"