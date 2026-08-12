import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.check import Check
from app.utils.face_recognition import verify_faces

router = APIRouter(prefix="/checks", tags=["Asistencias"])

@router.post("/mark")
def mark_attendance(
    employ_number: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.employ_number == employ_number).first()
    if not user or not user.face_img_path:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    registered_img_path = os.path.abspath(user.face_img_path)

    if not os.path.exists(registered_img_path):
        raise HTTPException(
            status_code=400, 
            detail=f"La foto del usuario no existe en el servidor: {registered_img_path}"
        )

    os.makedirs("uploads", exist_ok=True)
    temp_path = os.path.abspath(f"uploads/temp_{employ_number}.jpg")
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    is_match = verify_faces(registered_img_path, temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not is_match:
        raise HTTPException(status_code=401, detail="Autenticación fallida: El rostro no coincide.")

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # LÓGICA DE HORARIOS Y TOLERANCIA (9:00 AM + 15 min tolerancia)
    hora_limite = now.replace(hour=9, minute=15, second=0, microsecond=0)
    estado_registro = "OK" if now <= hora_limite else "RETARDO"

    existing_check = db.query(Check).filter(
        Check.user_id == user.id,
        Check.date == today_str
    ).first()

    if not existing_check:
        new_check = Check(
            user_id=user.id,
            check_in=now,
            check_out=None,
            state=estado_registro,
            date=today_str
        )
        db.add(new_check)
        db.commit()
        return {"message": f"Entrada registrada para {user.name} ({estado_registro}).", "type": "entrada"}
    
    elif existing_check.check_out is None:
        existing_check.check_out = now
        db.commit()
        return {"message": f"Salida registrada para {user.name}.", "type": "salida"}
    
    else:
        raise HTTPException(status_code=400, detail="Ya registraste entrada y salida por hoy.")

@router.get("/history")
def get_attendance_history(db: Session = Depends(get_db)):
    checks = db.query(Check).order_by(Check.check_in.desc()).all()
    history = []
    
    for check in checks:
        history.append({
            "id": check.id,
            "employ_number": check.user.employ_number,
            "employee_name": f"{check.user.name} {check.user.lastnames}",
            "date": check.date,
            "check_in": check.check_in.strftime("%H:%M:%S") if check.check_in else None,
            "check_out": check.check_out.strftime("%H:%M:%S") if check.check_out else None,
            "state": check.state
        })
        
    return history

@router.post("/request-leave")
def request_leave(
    employ_number: str = Form(...),
    reason: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.employ_number == employ_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    new_check = Check(
        user_id=user.id,
        check_in=now,
        check_out=now,
        state="PERMISO",
        date=today_str
    )
    db.add(new_check)
    db.commit()

    return {"message": f"Permiso registrado correctamente para {user.name}."}

@router.post("/simulate-late")
def simulate_late(
    employ_number: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.employ_number == employ_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    new_check = Check(
        user_id=user.id,
        check_in=now,
        check_out=None,
        state="RETARDO",
        date=today_str
    )
    db.add(new_check)
    db.commit()

    return {"message": f"Retardo registrado para {user.name}."}

@router.post("/mark-late")
def mark_late(
    employ_number: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.employ_number == employ_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    new_check = Check(
        user_id=user.id,
        check_in=now,
        check_out=None,
        state="RETARDO",
        date=today_str
    )
    db.add(new_check)
    db.commit()

    return {"message": f"Retardo registrado para {user.name}."}