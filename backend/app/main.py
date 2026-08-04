import sys
from pathlib import Path

# Añade la carpeta 'backend' al camino de búsqueda de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import engine, Base
from fastapi import FastAPI
from app.database import engine, Base
import app.models as models
from app.routes import users, checks, schedules, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Control de Asistencia Biométrica",
    version="1.0.0"
)

# Conectamos las 4 secciones de la API
app.include_router(users.router)
app.include_router(checks.router)
app.include_router(schedules.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"message": "Base de datos y rutas cargadas correctamente."}