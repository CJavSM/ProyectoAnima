import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-content">
            <h1 className="navbar-brand">Ánima</h1>
            <div className="navbar-user">
              <span className="navbar-username">
                Hola, <span>{user?.username || user?.first_name}</span>
              </span>
              <button onClick={handleLogout} className="btn-logout">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="dashboard-content">
        <div className="dashboard-card">
          <div className="dashboard-header">
            <h2 className="dashboard-title">¡Bienvenido a Ánima! 🎵</h2>
            <p className="dashboard-subtitle">
              Música que refleja cómo te sentís
            </p>
          </div>

          {/* User Info Card */}
          <div className="profile-card">
            <h3 className="profile-title">Tu Perfil</h3>
            <div className="profile-grid">
              <div className="profile-field">
                <span className="profile-label">Username</span>
                <p className="profile-value">{user?.username}</p>
              </div>
              <div className="profile-field">
                <span className="profile-label">Email</span>
                <p className="profile-value">{user?.email}</p>
              </div>
              {user?.first_name && (
                <div className="profile-field">
                  <span className="profile-label">Nombre</span>
                  <p className="profile-value">
                    {user.first_name} {user.last_name}
                  </p>
                </div>
              )}
              <div className="profile-field">
                <span className="profile-label">Estado</span>
                <p className="profile-value">
                  <span className={`badge ${user?.is_verified ? 'badge-success' : 'badge-warning'}`}>
                    {user?.is_verified ? '✓ Verificado' : '⏳ Pendiente de verificación'}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Coming Soon Features */}
          <div className="features-grid">
            <div className="feature-card feature-card-purple">
              <div className="feature-icon">📸</div>
              <h4 className="feature-title">Análisis de Emoción</h4>
              <p className="feature-description">
                Captura tu emoción y recibe música personalizada
              </p>
              <span className="badge badge-warning">Próximamente</span>
            </div>

            <div className="feature-card feature-card-blue">
              <div className="feature-icon">🎵</div>
              <h4 className="feature-title">Recomendaciones</h4>
              <p className="feature-description">
                Playlists de Spotify basadas en tu estado de ánimo
              </p>
              <span className="badge badge-warning">Próximamente</span>
            </div>

            <div className="feature-card feature-card-green">
              <div className="feature-icon">📊</div>
              <h4 className="feature-title">Historial</h4>
              <p className="feature-description">
                Revisa tus análisis y recomendaciones anteriores
              </p>
              <span className="badge badge-warning">Próximamente</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;