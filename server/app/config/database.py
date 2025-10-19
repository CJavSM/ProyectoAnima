from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Forzar que los valores de server/.env sobrescriban variables existentes
load_dotenv(override=True)

# Leer DATABASE_URL del entorno y asegurar driver psycopg v3
_raw_url = os.getenv("DATABASE_URL", "").strip()
if not _raw_url:
    raise RuntimeError("DATABASE_URL no está configurado en el entorno (.env)")

# Forzar el uso del driver psycopg v3 si el esquema es genérico 'postgresql://'
if _raw_url.startswith("postgresql://") and "+" not in _raw_url.split(":", 1)[0]:
    DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = _raw_url

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()