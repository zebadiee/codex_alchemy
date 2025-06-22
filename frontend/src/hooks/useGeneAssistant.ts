import { useState } from 'react';

export function useGeneAssistant() {
  const [output, setOutput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const invokeGene = async (prompt: string) => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/gene/invoke', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) throw new Error('Failed to invoke Gene');

      const data = await res.json();
setOutput(data.output || 'No response from Gene');    } catch (err: any) {
      setOutput(`❌ Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return { output, loading, invokeGene };
}
