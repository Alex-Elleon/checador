from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    since = Column(String, nullable=False) # "YYYY-MM-DD"
    to = Column(String, nullable=False)    # "YYYY-MM-DD"
    reason = Column(String, nullable=False)
    is_justified = Column(Boolean, default=False)
    url_file = Column(String, nullable=True)

    user = relationship("User", back_populates="reports")