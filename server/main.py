from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, emotion_routes, music_routes
import os
from dotenv import load_dotenv
from app.config.database import Base, engine
import logging

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Ánima API",
    description="API para detección de emociones y recomendación musical",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_routes.router)
app.include_router(emotion_routes.router)
app.include_router(music_routes.router)

# Ruta raíz
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Ánima API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "anima-api"
    }

# Crear tablas automáticamente al iniciar si no existen
@app.on_event("startup")
def on_startup():
    try:
        # Loggear URL de conexión (ocultando la contraseña)
        try:
            db_url_masked = engine.url.render_as_string(hide_password=True)
            logger.info(f"DB URL: {db_url_masked}")
        except Exception:
            logger.info("DB URL: <no disponible>")

        # Probar conexión simple
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")

        # Crear tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.exception("Error creando tablas en el arranque: %s", e)

# Health DB endpoint
@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            result = conn.exec_driver_sql("SELECT 1").scalar()
        return {"status": "ok", "result": result}
    except Exception as e:
        logger.exception("DB health check failed: %s", e)
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )