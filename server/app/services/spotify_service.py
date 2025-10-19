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
    
    # Mapeo de emociones a artistas representativos por género/estilo
    EMOTION_ARTISTS = {
        'HAPPY': [
            '3TVXtAsR1Inumwj472S9r4',  # Drake
            '1uNFoZAHBGtllmzznpCI3s',  # Justin Bieber
            '6vWDO969PvNqNYHIOW5v0m',  # Beyoncé
            '66CXWjxzNUsdJxJ2JdwvnR',  # Ariana Grande
            '6M2wZ9GZgrQXHCFfjv46we',  # Dua Lipa
            '5K4W6rqBFWDnAN6FQUkS6x',  # Kanye West
            '4gzpq5DPGxSnKTe4SA8HAU',  # Coldplay
            '0du5cEVh5yTK9QJze8zA0C',  # Bruno Mars
        ],
        'SAD': [
            '06HL4z0CvFAxyc27GXpf02',  # Taylor Swift
            '6S2OmqARrzebs0tKUEyXyp',  # Billie Eilish
            '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
            '00FQb4jTyendYWaN8pK0wa',  # Lana Del Rey
            '6l3HvQ5sa6mXTsMTB19rO5',  # J. Cole
            '5f7VJjfbwm532GiveGC0ZK',  # Lil Peep
            '4tZwfgrHOc3mvqYlEYSvVi',  # Daft Punk
            '7jy3rLJdDQY21OgRLCZ9sD',  # Foo Fighters
        ],
        'ANGRY': [
            '7dGJo4pcD2V6oG8kP0tJRR',  # Eminem
            '3qm84nBOXUEQ2vnTfUTTFC',  # Guns N' Roses
            '2ye2Wgw4gimLv2eAKyk1NB',  # Metallica
            '1Ffb6ejR6Fe5IamqA5oRUF',  # Nirvana
            '711MCceyCBcFnzjGY4Q7Un',  # AC/DC
            '6olE6TJLqED3rqDCT0FyPh',  # Nirvana
            '3RNrq3jvMZxD9ZyoOZbQOD',  # Kendrick Lamar (agresivo)
            '5K4W6rqBFWDnAN6FQUkS6x',  # Kanye West (agresivo)
        ],
        'CALM': [
            '6S2OmqARrzebs0tKUEyXyp',  # Billie Eilish
            '4gzpq5DPGxSnKTe4SA8HAU',  # Coldplay
            '3WrFJ7ztbogyGnTHbHJFl2',  # The Beatles
            '0oSGxfWSnnOXhD2fKuz2Gy',  # David Bowie
            '6eUKZXaKkcviH0Ku9w2n3V',  # Ed Sheeran
            '5pKCCKE2ajJHZ9KAiaK11H',  # Rihanna
            '1uNFoZAHBGtllmzznpCI3s',  # Justin Bieber (baladas)
            '53XhwfbYqKCa1cC15pYq2q',  # Imagine Dragons
        ],
        'SURPRISED': [
            '4tZwfgrHOc3mvqYlEYSvVi',  # Daft Punk
            '6M2wZ9GZgrQXHCFfjv46we',  # Dua Lipa
            '1anyVhU62p31KFi8MEzkbf',  # Marshmello
            '66CXWjxzNUsdJxJ2JdwvnR',  # Ariana Grande
            '5K4W6rqBFWDnAN6FQUkS6x',  # Kanye West
            '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
            '0du5cEVh5yTK9QJze8zA0C',  # Bruno Mars
            '6vWDO969PvNqNYHIOW5v0m',  # Beyoncé
        ],
        'FEAR': [
            '6S2OmqARrzebs0tKUEyXyp',  # Billie Eilish
            '1Ffb6ejR6Fe5IamqA5oRUF',  # Nirvana
            '00FQb4jTyendYWaN8pK0wa',  # Lana Del Rey
            '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
            '7jy3rLJdDQY21OgRLCZ9sD',  # Foo Fighters
            '2ye2Wgw4gimLv2eAKyk1NB',  # Metallica
            '4tZwfgrHOc3mvqYlEYSvVi',  # Daft Punk
            '6olE6TJLqED3rqDCT0FyPh',  # Nirvana
        ],
        'DISGUSTED': [
            '7dGJo4pcD2V6oG8kP0tJRR',  # Eminem
            '3qm84nBOXUEQ2vnTfUTTFC',  # Guns N' Roses
            '1Ffb6ejR6Fe5IamqA5oRUF',  # Nirvana
            '711MCceyCBcFnzjGY4Q7Un',  # AC/DC
            '2ye2Wgw4gimLv2eAKyk1NB',  # Metallica
            '06HL4z0CvFAxyc27GXpf02',  # Taylor Swift (revenge)
            '3RNrq3jvMZxD9ZyoOZbQOD',  # Kendrick Lamar
            '6l3HvQ5sa6mXTsMTB19rO5',  # J. Cole
        ],
        'CONFUSED': [
            '4tZwfgrHOc3mvqYlEYSvVi',  # Daft Punk
            '0oSGxfWSnnOXhD2fKuz2Gy',  # David Bowie
            '5K4W6rqBFWDnAN6FQUkS6x',  # Kanye West
            '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
            '6S2OmqARrzebs0tKUEyXyp',  # Billie Eilish
            '53XhwfbYqKCa1cC15pYq2q',  # Imagine Dragons
            '7jy3rLJdDQY21OgRLCZ9sD',  # Foo Fighters
            '3RNrq3jvMZxD9ZyoOZbQOD',  # Kendrick Lamar
        ]
    }
    
    # Playlists curadas de Spotify por emoción
    EMOTION_PLAYLISTS = {
        'HAPPY': ['37i9dQZF1DXdPec7aLTmlC', '37i9dQZF1DX3rxVfibe1L0', '37i9dQZF1DWSf2RDTDayIx'],  # Feel Good, Happy Hits, Mood Booster
        'SAD': ['37i9dQZF1DX3YSRoSdA634', '37i9dQZF1DWVrtsSlLKzro', '37i9dQZF1DX7qK8ma5wgG1'],  # Life Sucks, All Out 2010s, Sad Songs
        'ANGRY': ['37i9dQZF1DWWJOmJ7nRx0C', '37i9dQZF1DX1tyCD9QhIWF', '37i9dQZF1DWTcqUzwhNmKv'],  # Rock Hard, Rage Beats, Rock Classics
        'CALM': ['37i9dQZF1DWZd79rJ6a7lp', '37i9dQZF1DWYcDQ1hSjOpY', '37i9dQZF1DX4sWSpwq3LiO'],  # Chill Hits, Chill Vibes, Peaceful Piano
        'SURPRISED': ['37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX4dyzvuaRJ0n', '37i9dQZF1DX4JAvHpjipBk'],  # RapCaviar, Pop Rising, New Music Friday
        'FEAR': ['37i9dQZF1DWWvvyNmW9V9a', '37i9dQZF1DX1s9knjP51Oa', '37i9dQZF1DWXLeA8Omikj7'],  # Dark & Stormy, All Out 80s, Big on the Internet
        'DISGUSTED': ['37i9dQZF1DWWJOmJ7nRx0C', '37i9dQZF1DX1lVhptIYRda', '37i9dQZF1DX0hvV7a1tEWd'],  # Rock Hard, Rock This, Grunge
        'CONFUSED': ['37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DXdbXrPNafg9d', '37i9dQZF1DWWvvyNmW9V9a']  # RapCaviar, Alternative, Dark & Stormy
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
        Usa múltiples estrategias: artistas top tracks, playlists curadas, y álbumes
        
        Args:
            emotion: Emoción detectada (HAPPY, SAD, etc.)
            limit: Número de canciones a recomendar
            
        Returns:
            Dict con las recomendaciones
        """
        try:
            artists = self.EMOTION_ARTISTS.get(emotion, self.EMOTION_ARTISTS['CALM'])
            playlists = self.EMOTION_PLAYLISTS.get(emotion, self.EMOTION_PLAYLISTS['CALM'])
            
            logger.info(f"Buscando música para {emotion} usando {len(artists)} artistas y {len(playlists)} playlists")
            
            all_tracks = []
            seen_track_ids = set()
            
            # Estrategia 1: Top tracks de artistas representativos (60% del total)
            target_from_artists = int(limit * 0.6)
            selected_artists = random.sample(artists, min(4, len(artists)))
            
            for artist_id in selected_artists:
                try:
                    top_tracks = self.sp.artist_top_tracks(artist_id, country='US')
                    
                    for track in top_tracks['tracks'][:3]:  # Top 3 de cada artista
                        if track['id'] not in seen_track_ids and len(all_tracks) < target_from_artists:
                            track_info = self._process_track(track)
                            all_tracks.append(track_info)
                            seen_track_ids.add(track['id'])
                            
                except Exception as artist_error:
                    logger.warning(f"Error con artista {artist_id}: {str(artist_error)}")
                    continue
            
            logger.info(f"Obtenidas {len(all_tracks)} canciones de artistas")
            
            # Estrategia 2: Tracks de playlists curadas (40% del total)
            target_from_playlists = limit - len(all_tracks)
            selected_playlists = random.sample(playlists, min(2, len(playlists)))
            
            for playlist_id in selected_playlists:
                if len(all_tracks) >= limit:
                    break
                    
                try:
                    playlist_tracks = self.sp.playlist_tracks(playlist_id, limit=20, market='US')
                    
                    # Tomar tracks aleatorios de la playlist
                    random_tracks = random.sample(
                        playlist_tracks['items'], 
                        min(10, len(playlist_tracks['items']))
                    )
                    
                    for item in random_tracks:
                        if len(all_tracks) >= limit:
                            break
                            
                        track = item['track']
                        if track and track['id'] not in seen_track_ids:
                            track_info = self._process_track(track)
                            all_tracks.append(track_info)
                            seen_track_ids.add(track['id'])
                            
                except Exception as playlist_error:
                    logger.warning(f"Error con playlist {playlist_id}: {str(playlist_error)}")
                    continue
            
            logger.info(f"Total de canciones obtenidas: {len(all_tracks)}")
            
            # Si aún no tenemos suficientes, buscar álbumes recientes de los artistas
            if len(all_tracks) < limit:
                remaining = limit - len(all_tracks)
                for artist_id in selected_artists[:2]:
                    if len(all_tracks) >= limit:
                        break
                    
                    try:
                        albums = self.sp.artist_albums(artist_id, album_type='album', limit=2, country='US')
                        
                        for album in albums['items']:
                            if len(all_tracks) >= limit:
                                break
                                
                            album_tracks = self.sp.album_tracks(album['id'], limit=5)
                            
                            for track in album_tracks['items']:
                                if len(all_tracks) >= limit:
                                    break
                                    
                                if track['id'] not in seen_track_ids:
                                    # Obtener información completa del track
                                    full_track = self.sp.track(track['id'])
                                    track_info = self._process_track(full_track)
                                    all_tracks.append(track_info)
                                    seen_track_ids.add(track['id'])
                                    
                    except Exception as album_error:
                        logger.warning(f"Error con álbumes de {artist_id}: {str(album_error)}")
                        continue
            
            # Mezclar para variedad
            random.shuffle(all_tracks)
            
            # Ordenar por popularidad pero mantener algo de aleatoriedad
            all_tracks.sort(key=lambda x: x['popularity'] + random.randint(-10, 10), reverse=True)
            
            final_tracks = all_tracks[:limit]
            
            logger.info(f"Playlist final: {len(final_tracks)} canciones para {emotion}")
            
            return {
                'success': True,
                'emotion': emotion,
                'tracks': final_tracks,
                'total': len(final_tracks),
                'genres_used': [f"{len(selected_artists)} artistas", f"{len(selected_playlists)} playlists"],
                'music_params': {
                    'valence': 'Basado en artistas representativos',
                    'energy': 'Top tracks y playlists curadas',
                    'tempo': 'Variado según artista y estilo',
                    'mode': f'{emotion.title()} vibes'
                }
            }
            
        except Exception as e:
            logger.error(f"Error al obtener recomendaciones: {str(e)}")
            logger.exception("Detalles del error:")
            return {
                'success': False,
                'error': 'Error al obtener recomendaciones de Spotify',
                'details': str(e)
            }
    
    def _process_track(self, track: Dict) -> Dict:
        """Procesa la información de un track de Spotify"""
        return {
            'id': track['id'],
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album': track['album']['name'],
            'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'preview_url': track.get('preview_url'),
            'external_url': track['external_urls']['spotify'],
            'duration_ms': track['duration_ms'],
            'popularity': track.get('popularity', 0)
        }
    
    def get_track_audio_features(self, track_id: str) -> Dict:
        """Obtiene las características de audio de una canción"""
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