import axios from 'axios';

const api = axios.create({
  baseURL: `${import.meta.env.VITE_BACKEND_URL}/api`,
});

// Function to refresh token
async function refreshToken() {
  try {
    const refresh = localStorage.getItem('refreshToken');
    if (!refresh) throw new Error("No refresh token available");

    const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`, { refresh });
    console.log("Token refreshed");

    const newAccessToken = response.data.access;
    const newRefreshToken = response.data.refresh;
    localStorage.setItem('accessToken', newAccessToken);
    localStorage.setItem('refreshToken', newRefreshToken);
    // Optionally update expiration time
    const decoded = JSON.parse(atob(newAccessToken.split('.')[1])); // Decode JWT payload
    localStorage.setItem('tokenExpiration', String(decoded.exp * 1000)); // Convert to milliseconds

    return newAccessToken;
  } catch (error) {
    console.error('Failed to refresh token', error);
    localStorage.removeItem('accessToken'); // Clear expired token
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('tokenExpiration');
    return null;
  }
}

// Axios interceptor
api.interceptors.request.use(async (config) => {
  console.log("Using API to make a request");

  let token = localStorage.getItem('accessToken');
  const tokenExpiration = localStorage.getItem('tokenExpiration');

  // Check if the token is expired
  if (tokenExpiration && Date.now() >= parseInt(tokenExpiration)) {
    console.log("Token expired, attempting refresh");
    token = await refreshToken();
  }

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    console.log("No valid token available");
  }

  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;