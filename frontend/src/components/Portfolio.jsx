import { useState, useEffect } from 'react';
import api from '../services/api';
import './Portfolio.css';

const Portfolio = () => {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadPortfolio();
    const interval = setInterval(loadPortfolio, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const loadPortfolio = async () => {
    try {
      const data = await api.getPortfolio();
      setPortfolio(data);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading portfolio...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  const totalValue = portfolio.holdings.reduce((sum, holding) => sum + holding.current_value, 0);
  const totalInvested = portfolio.holdings.reduce(
    (sum, holding) => sum + holding.quantity * holding.avg_price,
    0
  );
  const totalPnL = totalValue - totalInvested;
  const totalPnLPercent = totalInvested > 0 ? (totalPnL / totalInvested) * 100 : 0;

  return (
    <div className="portfolio-container">
      <div className="portfolio-header">
        <h2>Portfolio</h2>
        <p className="user-id">User: {portfolio.user_id}</p>
      </div>

      <div className="portfolio-summary">
        <div className="summary-card">
          <div className="summary-label">Total Value</div>
          <div className="summary-value">₹{totalValue.toFixed(2)}</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Total Invested</div>
          <div className="summary-value">₹{totalInvested.toFixed(2)}</div>
        </div>
        <div className={`summary-card ${totalPnL >= 0 ? 'positive' : 'negative'}`}>
          <div className="summary-label">Total P&L</div>
          <div className="summary-value">
            ₹{totalPnL.toFixed(2)} ({totalPnLPercent.toFixed(2)}%)
          </div>
        </div>
      </div>

      <div className="holdings-section">
        <h3>Holdings</h3>
        {portfolio.holdings.length === 0 ? (
          <p className="empty-state">No holdings yet</p>
        ) : (
          <table className="holdings-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Avg Price</th>
                <th>Current Value</th>
                <th>P&L</th>
                <th>P&L %</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.holdings.map((holding) => {
                const invested = holding.quantity * holding.avg_price;
                const pnl = holding.current_value - invested;
                const pnlPercent = invested > 0 ? (pnl / invested) * 100 : 0;

                return (
                  <tr key={holding.symbol}>
                    <td className="symbol-cell">{holding.symbol}</td>
                    <td>{holding.quantity}</td>
                    <td>₹{holding.avg_price.toFixed(2)}</td>
                    <td>₹{holding.current_value.toFixed(2)}</td>
                    <td className={pnl >= 0 ? 'positive' : 'negative'}>
                      ₹{pnl.toFixed(2)}
                    </td>
                    <td className={pnl >= 0 ? 'positive' : 'negative'}>
                      {pnlPercent.toFixed(2)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Portfolio;

