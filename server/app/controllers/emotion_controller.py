from fastapi import HTTPException, status, UploadFile
from app.services.rekognition_service import rekognition_service
from app.schemas.emotion_schemas import EmotionAnalysisResponse, EmotionAnalysisError
import logging

logger = logging.getLogger(__name__)

class EmotionController:
    
    @staticmethod
    async def analyze_emotion(file: UploadFile) -> EmotionAnalysisResponse:
        """
        Analiza las emociones de una imagen cargada
        
        Args:
            file: Archivo de imagen cargado
            
        Returns:
            EmotionAnalysisResponse con los resultados del análisis
        """
        try:
            # Leer el archivo
            image_bytes = await file.read()
            
            # Validar la imagen
            validation = rekognition_service.validate_image(image_bytes)
            if not validation['valid']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=validation['error']
                )
            
            # Analizar emociones
            result = rekognition_service.detect_faces_and_emotions(image_bytes)
            
            if not result['success']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.get('error', 'Error al procesar la imagen')
                )
            
            return EmotionAnalysisResponse(**result)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en analyze_emotion: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar la imagen: {str(e)}"
            )