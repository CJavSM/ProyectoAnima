import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from typing import Dict, List
import logging
import random

load_dotenv()

logger = logging.getLogger(__name__)

class SpotifyService:
    """Servicio para obtener recomendaciones musicales de Spotify"""
    
    # Mapeo de emociones a parámetros musicales
    EMOTION_MUSIC_PARAMS = {
        'HAPPY': {
            'valence': (0.6, 1.0),      # Positividad alta
            'energy': (0.6, 1.0),       # Energía alta
            'danceability': (0.5, 1.0), # Bailable
            'tempo': (110, 150),        # Tempo alegre
            'mode': 1,                  # Tonalidad mayor
            'genres': ['pop', 'dance', 'happy', 'party', 'latin']
        },
        'SAD': {
            'valence': (0.0, 0.4),      # Positividad baja
            'energy': (0.2, 0.5),       # Energía baja
            'danceability': (0.2, 0.5),
            'tempo': (60, 100),         # Tempo lento
            'mode': 0,                  # Tonalidad menor
            'genres': ['sad', 'acoustic', 'piano', 'indie', 'blues']
        },
        'ANGRY': {
            'valence': (0.2, 0.5),
            'energy': (0.7, 1.0),       # Energía muy alta
            'danceability': (0.5, 0.8),
            'tempo': (120, 180),        # Tempo rápido y agresivo
            'mode': 0,
            'genres': ['rock', 'metal', 'punk', 'hard-rock', 'grunge']
        },
        'CALM': {
            'valence': (0.4, 0.7),      # Neutral a positivo
            'energy': (0.2, 0.5),       # Energía baja
            'danceability': (0.2, 0.5),
            'tempo': (60, 90),          # Tempo muy lento
            'mode': 1,
            'genres': ['chill', 'ambient', 'classical', 'meditation', 'jazz']
        },
        'SURPRISED': {
            'valence': (0.5, 0.8),
            'energy': (0.6, 0.9),
            'danceability': (0.5, 0.8),
            'tempo': (100, 140),
            'mode': 1,
            'genres': ['electronic', 'pop', 'indie', 'alternative', 'synth-pop']
        },
        'FEAR': {
            'valence': (0.1, 0.4),
            'energy': (0.3, 0.6),
            'danceability': (0.2, 0.5),
            'tempo': (80, 120),
            'mode': 0,
            'genres': ['dark', 'ambient', 'industrial', 'gothic', 'alternative']
        },
        'DISGUSTED': {
            'valence': (0.2, 0.5),
            'energy': (0.4, 0.7),
            'danceability': (0.3, 0.6),
            'tempo': (90, 130),
            'mode': 0,
            'genres': ['alternative', 'indie', 'rock', 'grunge', 'punk']
        },
        'CONFUSED': {
            'valence': (0.3, 0.6),
            'energy': (0.4, 0.7),
            'danceability': (0.3, 0.6),
            'tempo': (85, 115),
            'mode': 0,
            'genres': ['alternative', 'indie', 'experimental', 'psychedelic', 'art-pop']
        }
    }
    
    def __init__(self):
        """Inicializa el cliente de Spotify"""
        try:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                raise ValueError("Credenciales de Spotify no configuradas")
            
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            logger.info("Cliente de Spotify inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar Spotify: {str(e)}")
            raise
    
    def get_recommendations(self, emotion: str, limit: int = 20) -> Dict:
        """
        Obtiene recomendaciones musicales basadas en la emoción
        
        Args:
            emotion: Emoción detectada (HAPPY, SAD, etc.)
            limit: Número de canciones a recomendar (máx 100)
            
        Returns:
            Dict con las recomendaciones
        """
        try:
            # Obtener parámetros para la emoción
            params = self.EMOTION_MUSIC_PARAMS.get(
                emotion, 
                self.EMOTION_MUSIC_PARAMS['CALM']
            )
            
            # Seleccionar géneros aleatorios
            seed_genres = random.sample(params['genres'], min(3, len(params['genres'])))
            
            # Preparar parámetros de búsqueda
            search_params = {
                'seed_genres': seed_genres,
                'limit': limit,
                'target_valence': (params['valence'][0] + params['valence'][1]) / 2,
                'min_valence': params['valence'][0],
                'max_valence': params['valence'][1],
                'target_energy': (params['energy'][0] + params['energy'][1]) / 2,
                'min_energy': params['energy'][0],
                'max_energy': params['energy'][1],
                'target_danceability': (params['danceability'][0] + params['danceability'][1]) / 2,
                'min_danceability': params['danceability'][0],
                'max_danceability': params['danceability'][1],
                'target_tempo': (params['tempo'][0] + params['tempo'][1]) / 2,
                'min_tempo': params['tempo'][0],
                'max_tempo': params['tempo'][1],
                'mode': params['mode']
            }
            
            # Obtener recomendaciones
            recommendations = self.sp.recommendations(**search_params)
            
            # Procesar tracks
            tracks = []
            for track in recommendations['tracks']:
                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': track['album']['name'],
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                }
                tracks.append(track_info)
            
            return {
                'success': True,
                'emotion': emotion,
                'tracks': tracks,
                'total': len(tracks),
                'genres_used': seed_genres,
                'music_params': {
                    'valence': f"{params['valence'][0]:.2f} - {params['valence'][1]:.2f}",
                    'energy': f"{params['energy'][0]:.2f} - {params['energy'][1]:.2f}",
                    'tempo': f"{params['tempo'][0]} - {params['tempo'][1]} BPM",
                    'mode': 'Mayor' if params['mode'] == 1 else 'Menor'
                }
            }
            
        except Exception as e:
            logger.error(f"Error al obtener recomendaciones: {str(e)}")
            return {
                'success': False,
                'error': 'Error al obtener recomendaciones de Spotify',
                'details': str(e)
            }
    
    def get_track_audio_features(self, track_id: str) -> Dict:
        """
        Obtiene las características de audio de una canción
        
        Args:
            track_id: ID de la canción en Spotify
            
        Returns:
            Dict con las características de audio
        """
        try:
            features = self.sp.audio_features(track_id)[0]
            
            if not features:
                return {'success': False, 'error': 'No se encontraron características'}
            
            return {
                'success': True,
                'features': {
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'key': features['key'],
                    'loudness': features['loudness'],
                    'mode': features['mode'],
                    'speechiness': features['speechiness'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'valence': features['valence'],
                    'tempo': features['tempo'],
                    'duration_ms': features['duration_ms'],
                    'time_signature': features['time_signature']
                }
            }
            
        except Exception as e:
            logger.error(f"Error al obtener audio features: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_playlist_description(self, emotion: str) -> str:
        """Genera una descripción para la playlist basada en la emoción"""
        descriptions = {
            'HAPPY': '¡Música alegre y energética para celebrar tu felicidad! 🎉',
            'SAD': 'Canciones emotivas que acompañan tus momentos de reflexión 💙',
            'ANGRY': 'Música poderosa para canalizar tu energía 🔥',
            'CALM': 'Melodías relajantes para tu paz interior 🧘',
            'SURPRISED': 'Canciones que capturan ese momento de asombro ✨',
            'FEAR': 'Música que te acompaña en momentos de incertidumbre 🌙',
            'DISGUSTED': 'Canciones alternativas que expresan tu disgusto 🎸',
            'CONFUSED': 'Música experimental para tu estado de confusión 🌀'
        }
        return descriptions.get(emotion, 'Música personalizada según tu emoción 🎵')

# Instancia global del servicio
spotify_service = SpotifyService()