from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    state = Column(String, nullable=False) # "OK", "Retardo", "Falta"
    date = Column(String, nullable=False)  # "YYYY-MM-DD"

    user = relationship("User", back_populates="checks")