import api from '../config/api';

const STORAGE_KEYS = {
  token: 'token',
  user: 'user',
};

const saveSession = ({ access_token, user }) => {
  if (access_token) localStorage.setItem(STORAGE_KEYS.token, access_token);
  if (user) localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));
};

const clearSession = () => {
  localStorage.removeItem(STORAGE_KEYS.token);
  localStorage.removeItem(STORAGE_KEYS.user);
};

const getStoredUser = () => {
  const raw = localStorage.getItem(STORAGE_KEYS.user);
  try {
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

const login = async ({ username_or_email, password }) => {
  const { data } = await api.post('/api/auth/login', { username_or_email, password });
  // Esperamos que el backend devuelva: { access_token, user }
  saveSession(data);
  return data;
};

const register = async (payload) => {
  const { data } = await api.post('/api/auth/register', payload);
  return data;
};

const me = async () => {
  const { data } = await api.get('/api/auth/me');
  return data;
};

const logout = () => {
  clearSession();
};

export const authService = {
  login,
  register,
  me,
  logout,
  getStoredUser,
};
