import { useState, useEffect } from 'react';
import api from '../services/api';
import './Trades.css';

const Trades = () => {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadTrades();
    const interval = setInterval(loadTrades, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const loadTrades = async () => {
    try {
      const data = await api.getTrades();
      setTrades(data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)));
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading trades...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="trades-container">
      <div className="trades-header">
        <h2>Trade History</h2>
        <p className="trades-count">{trades.length} trades</p>
      </div>

      {trades.length === 0 ? (
        <p className="empty-state">No trades executed yet</p>
      ) : (
        <table className="trades-table">
          <thead>
            <tr>
              <th>Trade ID</th>
              <th>Order ID</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade) => (
              <tr key={trade.trade_id}>
                <td>{trade.trade_id.substring(0, 8)}...</td>
                <td>{trade.order_id.substring(0, 8)}...</td>
                <td className="symbol-cell">{trade.symbol}</td>
                <td>
                  <span className={`side-badge side-${trade.side.toLowerCase()}`}>
                    {trade.side}
                  </span>
                </td>
                <td>{trade.quantity}</td>
                <td>₹{trade.price.toFixed(2)}</td>
                <td>{new Date(trade.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Trades;

