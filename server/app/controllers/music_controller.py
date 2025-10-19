from fastapi import HTTPException, status
from app.services.spotify_service import spotify_service
from app.schemas.music_schemas import MusicRecommendationsResponse
import logging

logger = logging.getLogger(__name__)

class MusicController:
    
    @staticmethod
    def get_recommendations(emotion: str, limit: int = 20) -> MusicRecommendationsResponse:
        """
        Obtiene recomendaciones musicales basadas en la emoción
        
        Args:
            emotion: Emoción detectada
            limit: Número de canciones a recomendar
            
        Returns:
            MusicRecommendationsResponse con las recomendaciones
        """
        try:
            # Validar emoción
            valid_emotions = ['HAPPY', 'SAD', 'ANGRY', 'CALM', 'SURPRISED', 'FEAR', 'DISGUSTED', 'CONFUSED']
            if emotion.upper() not in valid_emotions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Emoción inválida. Debe ser una de: {', '.join(valid_emotions)}"
                )
            
            # Validar límite
            if limit < 1 or limit > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El límite debe estar entre 1 y 100"
                )
            
            # Obtener recomendaciones
            result = spotify_service.get_recommendations(emotion.upper(), limit)
            
            if not result['success']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result.get('error', 'Error al obtener recomendaciones')
                )
            
            # Agregar descripción de playlist
            result['playlist_description'] = spotify_service.create_playlist_description(emotion.upper())
            
            return MusicRecommendationsResponse(**result)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en get_recommendations: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener recomendaciones: {str(e)}"
            )