import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# 1. Obtenemos la ruta absoluta de la carpeta 'backend'
# __file__ es backend/app/database.py -> parent es app/ -> parent.parent es backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent

# 2. Se usa el archivo local app.db para almacenar la base de datos SQLite 
# 3. Definir la ruta absoluta hacia app.db
DB_PATH = BACKEND_DIR / "app.db"

# 4. Construir la URL de SQLite con la ruta absoluta de forma segura
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



