import { useEffect, useState } from 'react';

export default function GlyphViewer() {
  const [svg, setSvg] = useState('');
  const [error, setError] = useState('');

  const steps = 5;
  const grammar = 'default';

  const fetchGlyph = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/glyph/generate?steps=${steps}&grammar=${grammar}&format=svg`);
      if (!res.ok) throw new Error('Failed to fetch glyph');
      const text = await res.text();
      setSvg(text);
    } catch (err) {
      setError('Error fetching glyph: ' + err);
    }
  };

  useEffect(() => {
    fetchGlyph();
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>🧬 Glyph Viewer</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div dangerouslySetInnerHTML={{ __html: svg }} />
    </div>
  );
}

