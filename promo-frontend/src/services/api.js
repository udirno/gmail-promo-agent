import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const promoAPI = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Get all promos for user
  getPromos: async (userId = 'test_user') => {
    const response = await api.get(`/api/promos/${userId}`);
    return response.data;
  },

  // Get statistics
  getStats: async (userId = 'test_user') => {
    const response = await api.get(`/api/stats/${userId}`);
    return response.data;
  },

  // Trigger email scan
  scanEmails: async (userId = 'test_user') => {
    const response = await api.post('/api/scan', { user_id: userId });
    return response.data;
  },

  // Check Gmail connection status
  checkGmailStatus: async (userId = 'test_user') => {
    const response = await api.get(`/api/auth/status/${userId}`);
    return response.data;
  },

  // Start OAuth flow
  startOAuth: async (userId = 'test_user') => {
    const response = await api.get(`/api/auth/start?user_id=${userId}`);
    return response.data;
  },

  // Create user
  createUser: async (userId = 'test_user', email = 'test@example.com') => {
    const response = await api.post('/api/users', {
      user_id: userId,
      email: email
    });
    return response.data;
  },

  // Mark promo as used
  markAsUsed: async (userId, code) => {
    const response = await api.post(`/api/promos/${userId}/${code}/mark-used`);
    return response.data;
  },

  // Delete promo
  deletePromo: async (userId, code) => {
    const response = await api.delete(`/api/promos/${userId}/${code}`);
    return response.data;
  },
};

export default promoAPI;