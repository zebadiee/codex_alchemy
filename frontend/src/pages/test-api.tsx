import React, { useEffect, useState } from 'react';

const TestApiPage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const testApi = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/gene/rituals_with_glyphs');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
    setLoading(false);
  };

  useEffect(() => {
    testApi();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>API Test Page</h1>
      <button onClick={testApi} disabled={loading}>
        {loading ? 'Testing...' : 'Test API'}
      </button>
      
      {error && (
        <div style={{ color: 'red', margin: '10px 0' }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {data && (
        <div style={{ margin: '10px 0' }}>
          <h3>API Response:</h3>
          <pre style={{ background: '#f5f5f5', padding: '10px', overflow: 'auto' }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default TestApiPage; 