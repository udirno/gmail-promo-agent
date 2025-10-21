import React, { useState, useEffect } from 'react';
import promoAPI from './services/api';
import './App.css';

function App() {
  const [promos, setPromos] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);
  const [gmailConnected, setGmailConnected] = useState(false);

  // Load data on mount
  useEffect(() => {
    loadData();
    checkGmailStatus();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [promosData, statsData] = await Promise.all([
        promoAPI.getPromos(),
        promoAPI.getStats()
      ]);
      
      setPromos(promosData);
      setStats(statsData);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. Is the backend running on port 8000?');
    } finally {
      setLoading(false);
    }
  };

  const checkGmailStatus = async () => {
    try {
      const status = await promoAPI.checkGmailStatus();
      setGmailConnected(status.connected);
    } catch (err) {
      console.error('Error checking Gmail status:', err);
    }
  };

  const handleScan = async () => {
    try {
      setScanning(true);
      setError(null);
      
      await promoAPI.scanEmails();
      await loadData();
      
      alert('✅ Scan complete!');
    } catch (err) {
      console.error('Error scanning:', err);
      setError('Scan failed: ' + err.message);
    } finally {
      setScanning(false);
    }
  };

  const handleConnectGmail = async () => {
    try {
      const result = await promoAPI.startOAuth();
      window.open(result.authorization_url, '_blank');
      alert('Please authorize in the popup window, then click OK here and refresh the page.');
    } catch (err) {
      console.error('Error starting OAuth:', err);
      setError('OAuth failed: ' + err.message);
    }
  };

  const copyToClipboard = (code) => {
    navigator.clipboard.writeText(code);
    alert(`Copied: ${code}`);
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎟️ Promo Code Dashboard</h1>
        <div className="header-actions">
          {!gmailConnected && (
            <button className="btn btn-secondary" onClick={handleConnectGmail}>
              Connect Gmail
            </button>
          )}
          <button 
            className="btn btn-primary" 
            onClick={handleScan}
            disabled={scanning || !gmailConnected}
          >
            {scanning ? '⏳ Scanning...' : '🔄 Scan Emails'}
          </button>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {!gmailConnected && (
        <div className="warning-banner">
          📧 Gmail not connected. Click "Connect Gmail" to get started.
        </div>
      )}

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Promos</div>
            <div className="stat-value">{stats.total_promos}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Active</div>
            <div className="stat-value green">{stats.active_promos}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Expiring Soon</div>
            <div className="stat-value orange">{stats.expiring_soon}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Expired</div>
            <div className="stat-value red">{stats.expired_promos}</div>
          </div>
        </div>
      )}

      <div className="promos-section">
        <h2>Your Promo Codes ({promos.length})</h2>
        
        {promos.length === 0 ? (
          <div className="empty-state">
            <p>No promo codes yet!</p>
            {gmailConnected && <p>Click "Scan Emails" to find promos in your inbox.</p>}
          </div>
        ) : (
          <div className="promos-grid">
            {promos.map((promo, index) => (
              <div key={index} className="promo-card">
                <div className="promo-header">
                  <span className="merchant">{promo.merchant}</span>
                  <span className={`category-badge ${promo.category.toLowerCase()}`}>
                    {promo.category}
                  </span>
                </div>
                
                <div className="promo-code">
                  <code>{promo.code}</code>
                  <button 
                    className="copy-btn"
                    onClick={() => copyToClipboard(promo.code)}
                  >
                    📋 Copy
                  </button>
                </div>
                
                <div className="promo-details">
                  <p className="discount">💰 {promo.discount}</p>
                  {promo.expiration && (
                    <p className="expiration">
                      📅 Expires: {promo.expiration}
                    </p>
                  )}
                  {promo.urgency_text && (
                    <p className={`urgency ${promo.urgency_class}`}>
                      ⏰ {promo.urgency_text}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;