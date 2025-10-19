import { useState, useEffect } from 'react';
import musicService from '../../services/musicService';
import emotionService from '../../services/emotionService';
import './MusicRecommendations.css';

const MusicRecommendations = ({ emotion, emotionColor, onClose }) => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [playingPreview, setPlayingPreview] = useState(null);
  const [audioElement, setAudioElement] = useState(null);

  useEffect(() => {
    loadRecommendations();
    
    // Cleanup: detener audio al desmontar
    return () => {
      if (audioElement) {
        audioElement.pause();
        audioElement.src = '';
      }
    };
  }, [emotion]);

  const loadRecommendations = async () => {
    setLoading(true);
    setError('');

    const response = await musicService.getRecommendations(emotion, 20);

    if (response.success) {
      setRecommendations(response.data);
    } else {
      setError(response.error);
    }

    setLoading(false);
  };

  const togglePreview = (track) => {
    if (!track.preview_url) {
      alert('Esta canción no tiene preview disponible. Abre en Spotify para escucharla completa.');
      return;
    }

    // Si está reproduciendo este track, pausar
    if (playingPreview === track.id) {
      audioElement.pause();
      setPlayingPreview(null);
      return;
    }

    // Si hay otro audio reproduciéndose, detenerlo
    if (audioElement) {
      audioElement.pause();
    }

    // Crear nuevo audio y reproducir
    const audio = new Audio(track.preview_url);
    audio.volume = 0.5;
    
    audio.play();
    audio.onended = () => setPlayingPreview(null);
    
    setAudioElement(audio);
    setPlayingPreview(track.id);
  };

  const handleOpenInSpotify = (url) => {
    musicService.openInSpotify(url);
  };

  if (loading) {
    return (
      <div className="music-modal-overlay">
        <div className="music-modal">
          <div className="music-loading">
            <div className="spinner-large"></div>
            <p>Buscando la música perfecta para ti...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="music-modal-overlay">
        <div className="music-modal">
          <button onClick={onClose} className="modal-close">✕</button>
          <div className="music-error">
            <p className="error-icon">❌</p>
            <p>{error}</p>
            <button onClick={onClose} className="btn btn-primary">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="music-modal-overlay" onClick={onClose}>
      <div className="music-modal" onClick={(e) => e.stopPropagation()}>
        <div className="music-header" style={{ borderTopColor: emotionColor }}>
          <div className="music-header-content">
            <h2 className="music-title">
              {emotionService.getEmotionEmoji(emotion)} Tu Playlist Personalizada
            </h2>
            <p className="music-subtitle">{recommendations?.playlist_description}</p>
          </div>
          <button onClick={onClose} className="modal-close">✕</button>
        </div>

        <div className="music-info">
          <div className="music-stats">
            <div className="stat-item">
              <span className="stat-label">Canciones</span>
              <span className="stat-value">{recommendations?.total}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Géneros</span>
              <span className="stat-value">{recommendations?.genres_used.join(', ')}</span>
            </div>
          </div>

          <div className="music-params">
            <h3 className="params-title">Parámetros Musicales</h3>
            <div className="params-grid">
              <div className="param-item">
                <span className="param-icon">💚</span>
                <div>
                  <span className="param-label">Positividad</span>
                  <span className="param-value">{recommendations?.music_params.valence}</span>
                </div>
              </div>
              <div className="param-item">
                <span className="param-icon">⚡</span>
                <div>
                  <span className="param-label">Energía</span>
                  <span className="param-value">{recommendations?.music_params.energy}</span>
                </div>
              </div>
              <div className="param-item">
                <span className="param-icon">🎵</span>
                <div>
                  <span className="param-label">Tempo</span>
                  <span className="param-value">{recommendations?.music_params.tempo}</span>
                </div>
              </div>
              <div className="param-item">
                <span className="param-icon">🎹</span>
                <div>
                  <span className="param-label">Tonalidad</span>
                  <span className="param-value">{recommendations?.music_params.mode}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="tracks-container">
          <h3 className="tracks-title">Canciones Recomendadas</h3>
          <div className="tracks-list">
            {recommendations?.tracks.map((track, index) => (
              <div key={track.id} className="track-item">
                <div className="track-number">{index + 1}</div>
                
                <div className="track-image-container">
                  {track.album_image && (
                    <img 
                      src={track.album_image} 
                      alt={track.album} 
                      className="track-image"
                    />
                  )}
                  {track.preview_url && (
                    <button 
                      className="track-play-btn"
                      onClick={() => togglePreview(track)}
                    >
                      {playingPreview === track.id ? '⏸️' : '▶️'}
                    </button>
                  )}
                </div>

                <div className="track-info">
                  <div className="track-name">{track.name}</div>
                  <div className="track-artists">{track.artists.join(', ')}</div>
                  <div className="track-album">{track.album}</div>
                </div>

                <div className="track-details">
                  <span className="track-duration">
                    {musicService.formatDuration(track.duration_ms)}
                  </span>
                  <div className="track-popularity">
                    <span className="popularity-label">❤️</span>
                    <span className="popularity-value">{track.popularity}</span>
                  </div>
                </div>

                <button
                  className="track-spotify-btn"
                  onClick={() => handleOpenInSpotify(track.external_url)}
                  title="Abrir en Spotify"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MusicRecommendations;