import sys
from pathlib import Path

# Añade la carpeta 'backend' al camino de búsqueda de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
import app.models as models
from app.routes import users, checks, schedules, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Control de Asistencia Biométrica",
    version="1.0.0"
)

# Servir carpeta de imágenes localmente
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Conectamos las 4 secciones de la API
app.include_router(users.router)
app.include_router(checks.router)
app.include_router(schedules.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"message": "Base de datos y rutas cargadas correctamente con motor biométrico FaceNet."}