import { useState, useEffect } from 'react';
import './Instruments.css';

const Instruments = ({ instruments }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredInstruments = instruments.filter((inst) =>
    inst.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
    inst.exchange.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="instruments-container">
      <div className="instruments-header">
        <h2>Available Instruments</h2>
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by symbol or exchange..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {filteredInstruments.length === 0 ? (
        <p className="empty-state">No instruments found</p>
      ) : (
        <div className="instruments-grid">
          {filteredInstruments.map((instrument) => (
            <div key={instrument.symbol} className="instrument-card">
              <div className="instrument-header">
                <h3 className="instrument-symbol">{instrument.symbol}</h3>
                <span className="instrument-type">{instrument.instrument_type}</span>
              </div>
              <div className="instrument-details">
                <div className="detail-item">
                  <span className="detail-label">Exchange:</span>
                  <span className="detail-value">{instrument.exchange}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Last Traded Price:</span>
                  <span className="detail-value price">₹{instrument.last_traded_price.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Instruments;

