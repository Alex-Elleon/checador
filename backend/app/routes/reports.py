from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.report import Report

router = APIRouter(prefix="/reports", tags=["Vacaciones y Permisos"])

class ReportCreate(BaseModel):
    user_id: int
    since: str
    to: str
    reason: str
    is_justified: Optional[bool] = False

@router.post("/")
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report_data.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()

@router.get("/user/{user_id}")
def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    return db.query(Report).filter(Report.user_id == user_id).all()

@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Permiso no encontrado.")
    db.delete(report)
    db.commit()
    return {"message": "Permiso eliminado correctamente."}