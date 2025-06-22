import React, { useState, useEffect, useCallback } from 'react';
import Tree from 'react-d3-tree';
import { useAssistantContext } from '../hooks/assistant_context';

interface SigilNode {
  name: string;
  attributes?: {
    evolution?: string;
    mutations?: string;
    timestamp?: string;
    status?: 'stale' | 'active' | 'drifting';
  };
  children?: SigilNode[];
}

interface SigilTreeProps {
  sigilName?: string;
  className?: string;
}

const SigilTree: React.FC<SigilTreeProps> = ({ sigilName = 'default', className = '' }) => {
  const [treeData, setTreeData] = useState<SigilNode | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<SigilNode | null>(null);
  const { isStaleGlyph, isUnlinkedGlyph, isRapidDrift } = useAssistantContext();

  const fetchTreeData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/vault/vault/tree?sigil=${sigilName}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch tree data: ${response.statusText}`);
      }
      const data = await response.json();
      setTreeData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [sigilName]);

  useEffect(() => {
    fetchTreeData();
  }, [fetchTreeData]);

  const getNodeColor = (node: SigilNode): string => {
    if (isStaleGlyph(node.name)) return '#ff6b6b'; // Red for stale
    if (isRapidDrift(node.name)) return '#ffd93d'; // Yellow for drifting
    if (isUnlinkedGlyph(node.name)) return '#6c757d'; // Gray for unlinked
    return '#4ecdc4'; // Default teal
  };

  const getNodeSize = (node: SigilNode): number => {
    if (node.children && node.children.length > 0) return 12;
    return 8;
  };

  const renderCustomNode = ({ nodeDatum, toggleNode }: any) => (
    <g>
      <circle
        r={getNodeSize(nodeDatum)}
        fill={getNodeColor(nodeDatum)}
        stroke="#2c3e50"
        strokeWidth="2"
        onClick={toggleNode}
        style={{ cursor: 'pointer' }}
      />
      {nodeDatum.children && (
        <text
          x="15"
          y="-5"
          fontSize="12"
          fill="#2c3e50"
          textAnchor="start"
          dominantBaseline="middle"
        >
          {nodeDatum.children.length > 0 ? '▼' : '▶'}
        </text>
      )}
    </g>
  );

  const handleNodeClick = (node: any) => {
    if (node.data && node.data.name) {
      setSelectedNode(node.data);
    }
  };

  if (loading) {
    return (
      <div className={`sigil-tree-container ${className}`}>
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading symbolic lineage tree...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`sigil-tree-container ${className}`}>
        <div className="error-message">
          <h3>Symbolic Tree Error</h3>
          <p>{error}</p>
          <button onClick={fetchTreeData} className="retry-button">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  if (!treeData) {
    return (
      <div className={`sigil-tree-container ${className}`}>
        <div className="no-data">
          <h3>No Lineage Data</h3>
          <p>No symbolic lineage found for sigil: {sigilName}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`sigil-tree-container ${className}`}>
      <div className="tree-header">
        <h2>Symbolic Lineage Tree: {sigilName}</h2>
        <div className="tree-controls">
          <button onClick={fetchTreeData} className="refresh-button">
            🔄 Refresh
          </button>
          <div className="legend">
            <span className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#4ecdc4' }}></span>
              Active
            </span>
            <span className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#ff6b6b' }}></span>
              Stale
            </span>
            <span className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#ffd93d' }}></span>
              Drifting
            </span>
            <span className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#6c757d' }}></span>
              Unlinked
            </span>
          </div>
        </div>
      </div>

      <div className="tree-visualization">
        <Tree
          data={treeData}
          orientation="vertical"
          pathFunc="step"
          translate={{ x: 400, y: 50 }}
          nodeSize={{ x: 200, y: 100 }}
          separation={{ siblings: 1.5, nonSiblings: 2 }}
          zoom={0.8}
          scaleExtent={{ min: 0.1, max: 2 }}
          renderCustomNodeElement={renderCustomNode}
          onNodeClick={handleNodeClick}
        />
      </div>

      {selectedNode && (
        <div className="node-details">
          <h3>Selected Node: {selectedNode.name}</h3>
          <div className="node-attributes">
            {selectedNode.attributes?.evolution && (
              <p><strong>Evolution:</strong> {selectedNode.attributes.evolution}</p>
            )}
            {selectedNode.attributes?.mutations && (
              <p><strong>Mutations:</strong> {selectedNode.attributes.mutations}</p>
            )}
            {selectedNode.attributes?.timestamp && (
              <p><strong>Timestamp:</strong> {selectedNode.attributes.timestamp}</p>
            )}
            {selectedNode.attributes?.status && (
              <p><strong>Status:</strong> 
                <span className={`status-${selectedNode.attributes.status}`}>
                  {selectedNode.attributes.status}
                </span>
              </p>
            )}
          </div>
          <button onClick={() => setSelectedNode(null)} className="close-button">
            Close Details
          </button>
        </div>
      )}

      <style jsx>{`
        .sigil-tree-container {
          width: 100%;
          height: 600px;
          border: 2px solid #2c3e50;
          border-radius: 8px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          position: relative;
          overflow: hidden;
        }

        .tree-header {
          background: rgba(44, 62, 80, 0.9);
          color: white;
          padding: 15px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .tree-header h2 {
          margin: 0;
          font-size: 1.2rem;
          font-weight: 600;
        }

        .tree-controls {
          display: flex;
          align-items: center;
          gap: 20px;
        }

        .refresh-button, .retry-button, .close-button {
          background: #3498db;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          transition: background 0.3s;
        }

        .refresh-button:hover, .retry-button:hover, .close-button:hover {
          background: #2980b9;
        }

        .legend {
          display: flex;
          gap: 15px;
        }

        .legend-item {
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 12px;
        }

        .legend-color {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          border: 1px solid #2c3e50;
        }

        .tree-visualization {
          height: 500px;
          overflow: auto;
        }

        .loading-spinner, .error-message, .no-data {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: white;
          text-align: center;
        }

        .spinner {
          width: 40px;
          height: 40px;
          border: 4px solid rgba(255, 255, 255, 0.3);
          border-top: 4px solid white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 20px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .node-details {
          position: absolute;
          top: 80px;
          right: 20px;
          background: rgba(44, 62, 80, 0.95);
          color: white;
          padding: 20px;
          border-radius: 8px;
          max-width: 300px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        .node-details h3 {
          margin: 0 0 15px 0;
          font-size: 1.1rem;
          color: #3498db;
        }

        .node-attributes p {
          margin: 8px 0;
          font-size: 14px;
        }

        .status-stale { color: #ff6b6b; }
        .status-active { color: #4ecdc4; }
        .status-drifting { color: #ffd93d; }

        .error-message h3 {
          color: #e74c3c;
          margin-bottom: 10px;
        }

        .no-data h3 {
          color: #95a5a6;
          margin-bottom: 10px;
        }
      `}</style>
    </div>
  );
};

export default SigilTree; 