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
    file: UploadFile = File(...),  # Recibe únicamente UNA foto
    db: Session = Depends(get_db)
):
    # 1. Verificar si el número de empleado ya existe
    existing_user = db.query(User).filter(User.employ_number == employ_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El número de empleado ya está registrado.")

    # 2. Asegurar que exista la carpeta de destino
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 3. Guardar la imagen con el identificador del empleado
    file_path = os.path.join(UPLOAD_DIR, f"{employ_number}.jpg")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Registrar en la Base de Datos guardando la ruta del archivo JPG
    new_user = User(
        employ_number=employ_number,
        name=name,
        lastnames=lastnames,
        genre=genre,
        occupation=occupation,
        schedule_id=schedule_id,
        face_img_path=file_path  # Apunta al archivo JPG individual
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # 1. Eliminar archivo de imagen si existe físicamente
    if user.face_img_path and os.path.exists(user.face_img_path):
        os.remove(user.face_img_path)

    # 2. Eliminar usuario de la base de datos
    db.delete(user)
    db.commit()

    return {"message": f"Usuario {user.name} eliminado correctamente junto con su imagen."}

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

    # Registrar el permiso directamente en la tabla de asistencias
    new_check = Check(
        user_id=user.id,
        check_in=now,
        check_out=now,
        state="PERMISO",
        date=today_str
    )
    db.add(new_check)
    db.commit()

    return {"message": f"Permiso guardado correctamente para {user.name}."}