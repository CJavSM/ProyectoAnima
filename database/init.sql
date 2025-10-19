-- Crear extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    profile_picture VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Tabla de análisis de emociones
-- Nota: Por seguridad, NO se almacena la foto del usuario
CREATE TABLE emotion_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    dominant_emotion VARCHAR(50) NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    emotion_details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de recomendaciones musicales
CREATE TABLE music_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES emotion_analyses(id) ON DELETE CASCADE,
    spotify_playlist_id VARCHAR(255),
    playlist_name VARCHAR(255),
    tracks JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_emotion_analyses_user_id ON emotion_analyses(user_id);
CREATE INDEX idx_emotion_analyses_created_at ON emotion_analyses(created_at);
CREATE INDEX idx_music_recommendations_analysis_id ON music_recommendations(analysis_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at en users
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insertar usuario de prueba (contraseña: Test123!)
-- Hash generado con bcrypt rounds=12
INSERT INTO users (email, username, password_hash, first_name, last_name, is_verified)
VALUES (
    'test@anima.com',
    'testuser',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Fxj.1fWZKUxW',
    'Usuario',
    'Prueba',
    TRUE
);

-- Comentarios para documentación
COMMENT ON TABLE users IS 'Tabla principal de usuarios del sistema';
COMMENT ON TABLE emotion_analyses IS 'Registro de análisis de emociones realizados por los usuarios';
COMMENT ON TABLE music_recommendations IS 'Recomendaciones musicales basadas en análisis de emociones';