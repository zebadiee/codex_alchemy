import React, { useEffect, useState } from 'react';

const DebugPage: React.FC = () => {
  const [status, setStatus] = useState<string>('Initializing...');
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const testApi = async () => {
      setStatus('Testing API connection...');
      
      try {
        console.log('🔍 Testing API connection to http://localhost:8000/api/gene/rituals_with_glyphs');
        
        const response = await fetch('http://localhost:8000/api/gene/rituals_with_glyphs');
        console.log('📡 Response received:', response.status, response.statusText);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('✅ Data received:', result);
        
        setData(result);
        setStatus(`Success! Received ${result.length} rituals`);
        
      } catch (err) {
        console.error('❌ API test failed:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
        setStatus('Failed to connect to API');
      }
    };

    testApi();
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🔍 API Debug Page</h1>
      
      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
        <strong>Status:</strong> {status}
      </div>
      
      {error && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#ffebee', color: '#c62828' }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {data && (
        <div style={{ marginBottom: '20px' }}>
          <h3>📊 Received Data:</h3>
          <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', overflow: 'auto' }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
      
      <div style={{ marginTop: '20px' }}>
        <h3>🔗 Test Links:</h3>
        <ul>
          <li><a href="/rituals">Rituals Page</a></li>
          <li><a href="/glyphs">Glyphs Page</a></li>
          <li><a href="/">Dashboard</a></li>
        </ul>
      </div>
    </div>
  );
};

export default DebugPage; 