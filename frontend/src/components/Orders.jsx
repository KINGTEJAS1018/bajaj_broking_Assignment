import { useState, useEffect } from 'react';
import api from '../services/api';
import './Orders.css';

const Orders = ({ instruments }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    symbol: '',
    order_type: 'BUY',
    order_style: 'MARKET',
    quantity: '',
    price: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const orderData = {
        symbol: formData.symbol.toUpperCase(),
        order_type: formData.order_type,
        order_style: formData.order_style,
        quantity: parseInt(formData.quantity),
        price: formData.order_style === 'LIMIT' ? parseFloat(formData.price) : null,
      };

      const newOrder = await api.placeOrder(orderData);
      setOrders((prev) => [newOrder, ...prev]);
      
      // Reset form
      setFormData({
        symbol: '',
        order_type: 'BUY',
        order_style: 'MARKET',
        quantity: '',
        price: '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (orderId) => {
    try {
      const updatedOrder = await api.cancelOrder(orderId);
      setOrders((prev) =>
        prev.map((order) => (order.order_id === orderId ? updatedOrder : order))
      );
    } catch (err) {
      setError(err.message);
    }
  };

  const getStateColor = (state) => {
    switch (state) {
      case 'EXECUTED':
        return 'green';
      case 'CANCELLED':
        return 'red';
      case 'PLACED':
        return 'blue';
      default:
        return 'gray';
    }
  };

  return (
    <div className="orders-container">
      <div className="orders-header">
        <h2>Place Order</h2>
      </div>

      <form onSubmit={handleSubmit} className="order-form">
        <div className="form-row">
          <div className="form-group">
            <label>Symbol</label>
            <input
              type="text"
              value={formData.symbol}
              onChange={(e) => setFormData({ ...formData, symbol: e.target.value })}
              placeholder="e.g., ABC"
              required
              list="symbols"
            />
            <datalist id="symbols">
              {instruments.map((inst) => (
                <option key={inst.symbol} value={inst.symbol} />
              ))}
            </datalist>
          </div>

          <div className="form-group">
            <label>Order Type</label>
            <select
              value={formData.order_type}
              onChange={(e) => setFormData({ ...formData, order_type: e.target.value })}
              required
            >
              <option value="BUY">BUY</option>
              <option value="SELL">SELL</option>
            </select>
          </div>

          <div className="form-group">
            <label>Order Style</label>
            <select
              value={formData.order_style}
              onChange={(e) => setFormData({ ...formData, order_style: e.target.value })}
              required
            >
              <option value="MARKET">MARKET</option>
              <option value="LIMIT">LIMIT</option>
            </select>
          </div>

          <div className="form-group">
            <label>Quantity</label>
            <input
              type="number"
              value={formData.quantity}
              onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
              placeholder="Enter quantity"
              min="1"
              required
            />
          </div>

          {formData.order_style === 'LIMIT' && (
            <div className="form-group">
              <label>Price</label>
              <input
                type="number"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                placeholder="Enter price"
                step="0.01"
                min="0"
                required
              />
            </div>
          )}

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Placing...' : 'Place Order'}
          </button>
        </div>
      </form>

      {error && <div className="error-message">{error}</div>}

      <div className="orders-list">
        <h3>Recent Orders</h3>
        {orders.length === 0 ? (
          <p className="empty-state">No orders placed yet</p>
        ) : (
          <table className="orders-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Symbol</th>
                <th>Type</th>
                <th>Style</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>State</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.order_id}>
                  <td>{order.order_id.substring(0, 8)}...</td>
                  <td>{order.symbol}</td>
                  <td>{order.order_type}</td>
                  <td>{order.order_style}</td>
                  <td>{order.quantity}</td>
                  <td>{order.price || 'N/A'}</td>
                  <td>
                    <span className={`state-badge state-${getStateColor(order.state)}`}>
                      {order.state}
                    </span>
                  </td>
                  <td>{new Date(order.created_at).toLocaleString()}</td>
                  <td>
                    {order.state === 'PLACED' && (
                      <button
                        onClick={() => handleCancel(order.order_id)}
                        className="btn-cancel"
                      >
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Orders;

