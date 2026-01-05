import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, API_KEYS } from '../contexts/AuthContext';
import './Login.css';

const Login = () => {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    try {
      login(apiKey);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDemoLogin = (key) => {
    setApiKey(key);
    try {
      login(key);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Bajaj Broking</h1>
        <p className="subtitle">Trading Platform</p>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="apiKey">API Key</label>
            <input
              type="text"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your API key"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-primary">
            Login
          </button>
        </form>

        <div className="demo-keys">
          <p>Demo API Keys:</p>
          <div className="demo-buttons">
            <button
              type="button"
              onClick={() => handleDemoLogin('demo-key')}
              className="btn-demo"
            >
              Demo User
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('alice-key')}
              className="btn-demo"
            >
              Alice
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('bob-key')}
              className="btn-demo"
            >
              Bob
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

