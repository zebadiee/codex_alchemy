import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import SigilTree from '../components/SigilTree';

const SigilTreePage: React.FC = () => {
  const [selectedSigil, setSelectedSigil] = useState('default');
  const [availableSigils, setAvailableSigils] = useState<string[]>(['default', 'fireball', 'ritual']);

  const handleSigilChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedSigil(event.target.value);
  };

  return (
    <div className="sigil-tree-page">
      <Head>
        <title>Symbolic Lineage Tree - Codex Alchemy</title>
        <meta name="description" content="Interactive symbolic lineage tree visualization for Codex Alchemy" />
      </Head>

      <div className="page-header">
        <div className="header-content">
          <h1>🧬 Symbolic Lineage Tree</h1>
          <p>Visualize the evolutionary paths of your symbolic constructs</p>
        </div>
        <div className="header-actions">
          <Link href="/" className="back-button">
            ← Back to Dashboard
          </Link>
        </div>
      </div>

      <div className="tree-controls">
        <div className="sigil-selector">
          <label htmlFor="sigil-select">Select Sigil:</label>
          <select
            id="sigil-select"
            value={selectedSigil}
            onChange={handleSigilChange}
            className="sigil-dropdown"
          >
            {availableSigils.map((sigil) => (
              <option key={sigil} value={sigil}>
                {sigil.charAt(0).toUpperCase() + sigil.slice(1)}
              </option>
            ))}
          </select>
        </div>
        
        <div className="tree-info">
          <div className="info-card">
            <h3>📊 Tree Statistics</h3>
            <ul>
              <li><strong>Active Nodes:</strong> <span className="stat-active">12</span></li>
              <li><strong>Stale Nodes:</strong> <span className="stat-stale">3</span></li>
              <li><strong>Drifting Nodes:</strong> <span className="stat-drifting">2</span></li>
              <li><strong>Total Evolution:</strong> <span className="stat-total">17</span></li>
            </ul>
          </div>
        </div>
      </div>

      <div className="tree-container">
        <SigilTree sigilName={selectedSigil} />
      </div>

      <div className="tree-legend">
        <h3>Symbolic Status Legend</h3>
        <div className="legend-grid">
          <div className="legend-item">
            <span className="legend-color active"></span>
            <span className="legend-text">
              <strong>Active:</strong> Currently evolving and stable
            </span>
          </div>
          <div className="legend-item">
            <span className="legend-color stale"></span>
            <span className="legend-text">
              <strong>Stale:</strong> No recent mutations or evolution
            </span>
          </div>
          <div className="legend-item">
            <span className="legend-color drifting"></span>
            <span className="legend-text">
              <strong>Drifting:</strong> Rapid changes detected
            </span>
          </div>
          <div className="legend-item">
            <span className="legend-color unlinked"></span>
            <span className="legend-text">
              <strong>Unlinked:</strong> No connections to main lineage
            </span>
          </div>
        </div>
      </div>

      <style jsx>{`
        .sigil-tree-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
          color: white;
          padding: 20px;
        }

        .page-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          padding: 20px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          backdrop-filter: blur(10px);
        }

        .header-content h1 {
          margin: 0 0 10px 0;
          font-size: 2.5rem;
          font-weight: 700;
          background: linear-gradient(45deg, #4ecdc4, #44a08d);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .header-content p {
          margin: 0;
          font-size: 1.1rem;
          opacity: 0.9;
        }

        .back-button {
          background: #3498db;
          color: white;
          text-decoration: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.3s ease;
        }

        .back-button:hover {
          background: #2980b9;
          transform: translateY(-2px);
        }

        .tree-controls {
          display: grid;
          grid-template-columns: 1fr 300px;
          gap: 20px;
          margin-bottom: 30px;
        }

        .sigil-selector {
          background: rgba(255, 255, 255, 0.1);
          padding: 20px;
          border-radius: 12px;
          backdrop-filter: blur(10px);
        }

        .sigil-selector label {
          display: block;
          margin-bottom: 10px;
          font-weight: 600;
          font-size: 1.1rem;
        }

        .sigil-dropdown {
          width: 100%;
          padding: 12px;
          border: none;
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.9);
          color: #2c3e50;
          font-size: 1rem;
          font-weight: 500;
        }

        .tree-info {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .info-card {
          background: rgba(255, 255, 255, 0.1);
          padding: 20px;
          border-radius: 12px;
          backdrop-filter: blur(10px);
        }

        .info-card h3 {
          margin: 0 0 15px 0;
          font-size: 1.2rem;
          color: #4ecdc4;
        }

        .info-card ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .info-card li {
          margin: 8px 0;
          font-size: 0.95rem;
        }

        .stat-active { color: #4ecdc4; font-weight: 600; }
        .stat-stale { color: #ff6b6b; font-weight: 600; }
        .stat-drifting { color: #ffd93d; font-weight: 600; }
        .stat-total { color: #3498db; font-weight: 600; }

        .tree-container {
          margin-bottom: 30px;
        }

        .tree-legend {
          background: rgba(255, 255, 255, 0.1);
          padding: 25px;
          border-radius: 12px;
          backdrop-filter: blur(10px);
        }

        .tree-legend h3 {
          margin: 0 0 20px 0;
          font-size: 1.3rem;
          color: #4ecdc4;
        }

        .legend-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 15px;
        }

        .legend-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 10px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 8px;
        }

        .legend-color {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          border: 2px solid rgba(255, 255, 255, 0.3);
        }

        .legend-color.active { background-color: #4ecdc4; }
        .legend-color.stale { background-color: #ff6b6b; }
        .legend-color.drifting { background-color: #ffd93d; }
        .legend-color.unlinked { background-color: #6c757d; }

        .legend-text {
          font-size: 0.95rem;
          line-height: 1.4;
        }

        @media (max-width: 768px) {
          .tree-controls {
            grid-template-columns: 1fr;
          }
          
          .page-header {
            flex-direction: column;
            gap: 20px;
            text-align: center;
          }
          
          .header-content h1 {
            font-size: 2rem;
          }
        }
      `}</style>
    </div>
  );
};

export default SigilTreePage; 