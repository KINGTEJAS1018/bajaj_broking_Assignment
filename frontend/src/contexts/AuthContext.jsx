import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Available API keys for demo
export const API_KEYS = {
  'demo-key': 'demo-user',
  'alice-key': 'alice',
  'bob-key': 'bob',
};

export const AuthProvider = ({ children }) => {
  const [apiKey, setApiKey] = useState(() => {
    return localStorage.getItem('apiKey');
  });
  const [user, setUser] = useState(() => {
    const key = localStorage.getItem('apiKey');
    return key ? API_KEYS[key] : null;
  });

  const login = (key) => {
    if (!API_KEYS[key]) {
      throw new Error('Invalid API key');
    }
    localStorage.setItem('apiKey', key);
    setApiKey(key);
    setUser(API_KEYS[key]);
  };

  const logout = () => {
    localStorage.removeItem('apiKey');
    setApiKey(null);
    setUser(null);
  };

  const isAuthenticated = !!apiKey;

  return (
    <AuthContext.Provider value={{ apiKey, user, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

