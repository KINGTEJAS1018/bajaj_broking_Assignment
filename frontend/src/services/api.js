const API_BASE_URL = 'http://localhost:8000/api/v1';

// Get API key from localStorage
const getApiKey = () => {
  return localStorage.getItem('apiKey');
};

// Make authenticated API request
const apiRequest = async (endpoint, options = {}) => {
  const apiKey = getApiKey();
  
  if (!apiKey) {
    throw new Error('No API key found. Please login.');
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// API methods
export const api = {
  // Instruments
  getInstruments: () => apiRequest('/instruments'),
  getInstrument: (symbol) => apiRequest(`/instruments/${symbol}`),

  // Orders
  placeOrder: (orderData) => apiRequest('/orders', {
    method: 'POST',
    body: JSON.stringify(orderData),
  }),
  cancelOrder: (orderId) => apiRequest(`/orders/${orderId}/cancel`, {
    method: 'POST',
  }),
  getOrder: (orderId) => apiRequest(`/orders/${orderId}`),

  // Portfolio
  getPortfolio: () => apiRequest('/portfolio'),

  // Trades
  getTrades: () => apiRequest('/trades'),
};

export default api;

