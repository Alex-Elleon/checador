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
    # Buscar usuario
    user = db.query(User).filter(User.employ_number == employ_number).first()
    if not user or not user.face_img_path:
        raise HTTPException(status_code=404, detail="Usuario o registro facial no encontrado.")

    # Guardar temporalmente la foto enviada para escaneo
    temp_path = f"uploads/temp_{employ_number}.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Comparación biométrica con DeepFace
    is_match = verify_faces(user.face_img_path, temp_path)

    # Eliminar imagen temporal
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not is_match:
        raise HTTPException(status_code=401, detail="Autenticación fallida: El rostro no coincide.")

    # Registrar hora y asistencia
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    new_check = Check(
        user_id=user.id,
        check_in=now,
        state="OK",
        date=today_str
    )
    db.add(new_check)
    db.commit()

    return {"message": "Asistencia registrada correctamente.", "user": user.name, "timestamp": now}