'use client';

import { useState } from 'react';
import { useGeneAssistant } from '../hooks/useGeneAssistant';

export default function GenePanel() {
  const [input, setInput] = useState('');
  const { output, loading, invokeGene } = useGeneAssistant();

  const handleSubmit = async () => {
    if (!input.trim()) return;
    await invokeGene(input);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🧠 Gene Assistant</h2>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={4}
        cols={60}
        style={{ display: 'block', marginBottom: 10 }}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Thinking...' : 'Invoke Gene'}
      </button>
      {output && (
        <pre style={{ marginTop: 20, backgroundColor: '#f4f4f4', padding: 10 }}>
          {output}
        </pre>
      )}
    </div>
  );
}
