from fastapi import APIRouter, Depends, UploadFile, File, status
from app.controllers.emotion_controller import EmotionController
from app.schemas.emotion_schemas import EmotionAnalysisResponse
from app.middlewares.auth_middleware import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/api/emotions",
    tags=["Análisis de Emociones"]
)

@router.post(
    "/analyze",
    response_model=EmotionAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analizar emociones en imagen",
    description="Analiza las emociones faciales en una imagen usando AWS Rekognition"
)
async def analyze_emotion(
    file: UploadFile = File(..., description="Imagen a analizar (JPG, PNG, WEBP - Máx. 5MB)"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analiza las emociones en una imagen:
    
    - **file**: Archivo de imagen (JPG, PNG, WEBP)
    - Tamaño máximo: 5MB
    - Debe contener al menos un rostro visible
    
    Retorna:
    - Emoción dominante y nivel de confianza
    - Todas las emociones detectadas con sus porcentajes
    - Detalles adicionales del rostro (edad estimada, género, etc.)
    """
    return await EmotionController.analyze_emotion(file)