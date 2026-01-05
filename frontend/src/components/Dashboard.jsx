import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import Orders from './Orders';
import Portfolio from './Portfolio';
import Trades from './Trades';
import Instruments from './Instruments';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('orders');
  const [instruments, setInstruments] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const wsUrl = 'ws://localhost:8000/api/v1/ws';
  const { messages, isConnected } = useWebSocket(wsUrl);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const loadInstruments = async () => {
      try {
        const data = await api.getInstruments();
        setInstruments(data);
      } catch (error) {
        console.error('Error loading instruments:', error);
      } finally {
        setLoading(false);
      }
    };

    loadInstruments();
  }, [user, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Bajaj Broking Trading Platform</h1>
          <div className="header-right">
            <div className="user-info">
              <span className="user-name">Welcome, {user}</span>
              <span className={`ws-status ${isConnected ? 'connected' : 'disconnected'}`}>
                {isConnected ? '● Connected' : '○ Disconnected'}
              </span>
            </div>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={activeTab === 'orders' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('orders')}
        >
          Orders
        </button>
        <button
          className={activeTab === 'portfolio' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('portfolio')}
        >
          Portfolio
        </button>
        <button
          className={activeTab === 'trades' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('trades')}
        >
          Trades
        </button>
        <button
          className={activeTab === 'instruments' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('instruments')}
        >
          Instruments
        </button>
      </nav>

      <main className="dashboard-content">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {activeTab === 'orders' && <Orders instruments={instruments} />}
            {activeTab === 'portfolio' && <Portfolio />}
            {activeTab === 'trades' && <Trades />}
            {activeTab === 'instruments' && <Instruments instruments={instruments} />}
          </>
        )}
      </main>
    </div>
  );
};

export default Dashboard;

