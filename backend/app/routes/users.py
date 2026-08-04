import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Usuarios"])

UPLOAD_DIR = "uploads"

@router.post("/register", response_model=UserResponse)
def create_user(
    employ_number: str = Form(...),
    name: str = Form(...),
    lastnames: str = Form(...),
    genre: str = Form(None),
    occupation: str = Form(None),
    schedule_id: int = Form(None),
    file: UploadFile = File(...),  # Foto de rostro capturada
    db: Session = Depends(get_db)
):
    # Verificar si el número de empleado ya existe
    existing_user = db.query(User).filter(User.employ_number == employ_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El número de empleado ya está registrado.")

    # Guardar la imagen localmente
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{employ_number}.jpg")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Crear usuario en Base de Datos
    new_user = User(
        employ_number=employ_number,
        name=name,
        lastnames=lastnames,
        genre=genre,
        occupation=occupation,
        schedule_id=schedule_id,
        face_img_path=file_path
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()