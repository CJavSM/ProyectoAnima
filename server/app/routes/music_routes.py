from fastapi import APIRouter, Depends, Query, status
from app.controllers.music_controller import MusicController
from app.schemas.music_schemas import MusicRecommendationsResponse
from app.middlewares.auth_middleware import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/api/music",
    tags=["Recomendaciones Musicales"]
)

@router.get(
    "/recommendations/{emotion}",
    response_model=MusicRecommendationsResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener recomendaciones musicales",
    description="Obtiene recomendaciones de canciones de Spotify basadas en la emoción detectada"
)
def get_music_recommendations(
    emotion: str,
    limit: int = Query(20, ge=1, le=100, description="Número de canciones a recomendar"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene recomendaciones musicales personalizadas:
    
    - **emotion**: Emoción detectada (HAPPY, SAD, ANGRY, CALM, SURPRISED, FEAR, DISGUSTED, CONFUSED)
    - **limit**: Número de canciones (1-100, default: 20)
    
    Las recomendaciones se basan en:
    - **Valence**: Nivel de positividad musical
    - **Energy**: Nivel de intensidad y actividad
    - **Tempo**: Velocidad en BPM (beats por minuto)
    - **Mode**: Tonalidad (Mayor o Menor)
    - **Danceability**: Qué tan bailable es la canción
    
    Retorna una lista de canciones con:
    - Información del track (nombre, artistas, álbum)
    - URL de Spotify
    - Preview de audio (si disponible)
    - Imagen del álbum
    """
    return MusicController.get_recommendations(emotion, limit)