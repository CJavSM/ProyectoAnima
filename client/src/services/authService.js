import api from '../config/api';

const STORAGE_KEYS = {
  token: 'token',
  user: 'user',
};

const saveSession = ({ access_token, user }) => {
  console.log('💾 [AuthService] Guardando sesión');
  if (access_token) localStorage.setItem(STORAGE_KEYS.token, access_token);
  if (user) localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));
};

const clearSession = () => {
  console.log('🗑️  [AuthService] Limpiando sesión');
  localStorage.removeItem(STORAGE_KEYS.token);
  localStorage.removeItem(STORAGE_KEYS.user);
};

const getStoredUser = () => {
  const raw = localStorage.getItem(STORAGE_KEYS.user);
  try {
    return raw ? JSON.parse(raw) : null;
  } catch {
    console.error('❌ [AuthService] Error parseando usuario almacenado');
    return null;
  }
};

const login = async ({ username_or_email, password }) => {
  console.log('🔑 [AuthService] Iniciando login para:', username_or_email);
  console.log('📡 [AuthService] URL del API:', api.defaults.baseURL);
  
  try {
    console.log('⏳ [AuthService] Enviando petición a /api/auth/login...');
    
    const { data } = await api.post('/api/auth/login', { 
      username_or_email, 
      password 
    });
    
    console.log('✅ [AuthService] Login exitoso:', {
      user: data.user?.username,
      hasToken: !!data.access_token
    });
    
    saveSession(data);
    return data;
    
  } catch (error) {
    console.error('❌ [AuthService] Error en login:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      code: error.code
    });

    // Mensajes de error más útiles
    if (error.code === 'ERR_NETWORK') {
      throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté corriendo.');
    }
    
    if (error.code === 'ECONNABORTED') {
      throw new Error('La petición tardó demasiado. Intenta de nuevo.');
    }

    if (error.response?.status === 401) {
      throw new Error(error.response.data?.detail || 'Credenciales incorrectas');
    }

    if (error.response?.status === 400) {
      throw new Error(error.response.data?.detail || 'Datos inválidos');
    }

    if (error.response?.status === 500) {
      throw new Error('Error del servidor. Intenta más tarde.');
    }

    throw error;
  }
};

const register = async (payload) => {
  console.log('📝 [AuthService] Registrando usuario:', payload.username);
  console.log('📡 [AuthService] URL del API:', api.defaults.baseURL);
  
  try {
    console.log('⏳ [AuthService] Enviando petición a /api/auth/register...');
    
    const { data } = await api.post('/api/auth/register', payload);
    
    console.log('✅ [AuthService] Registro exitoso:', data);
    
    return data;
    
  } catch (error) {
    console.error('❌ [AuthService] Error en registro:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      code: error.code
    });

    // Mensajes de error más útiles
    if (error.code === 'ERR_NETWORK') {
      throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté corriendo.');
    }

    if (error.response?.status === 400) {
      const detail = error.response.data?.detail;
      if (typeof detail === 'string') {
        throw new Error(detail);
      }
      // Si detail es un array (errores de validación)
      if (Array.isArray(detail)) {
        const messages = detail.map(err => err.msg || err.message).join(', ');
        throw new Error(messages);
      }
      throw new Error('Datos inválidos. Verifica el formulario.');
    }

    if (error.response?.status === 422) {
      throw new Error('Error de validación. Verifica los datos ingresados.');
    }

    if (error.response?.status === 500) {
      throw new Error('Error del servidor. Intenta más tarde.');
    }

    throw error;
  }
};

const me = async () => {
  console.log('👤 [AuthService] Obteniendo usuario actual');
  
  try {
    const { data } = await api.get('/api/auth/me');
    console.log('✅ [AuthService] Usuario obtenido:', data.username);
    return data;
  } catch (error) {
    console.error('❌ [AuthService] Error obteniendo usuario:', error);
    throw error;
  }
};

const logout = () => {
  console.log('👋 [AuthService] Cerrando sesión');
  clearSession();
};

export const authService = {
  login,
  register,
  me,
  logout,
  getStoredUser,
};