import React, { useState } from 'react';

interface RitualButtonsProps {
  glyph: any;
  setGlyphSvg: (svg: string, glyphJson?: any) => void;
}

const rituals = [
  {
    label: 'Evolve',
    color: '#0070f3',
    tooltip: '🧬 Evolve: Start glyph evolution (new glyph using current grammar).',
    endpoint: '/api/glyph/evolve',
    method: 'POST',
    body: () => ({ steps: 5, grammar: 'default', format: 'svg' }),
    assistant: 'Evolve will iterate this glyph using the current grammar and create a new variant.'
  },
  {
    label: 'Compress',
    color: '#10b981',
    tooltip: '🧱 Compress: Apply compression logic to current glyph.',
    endpoint: '/api/glyph/compress',
    method: 'POST',
    body: (glyph: any) => ({ glyph, format: 'json' }),
    assistant: 'Compress will deduplicate and shrink the glyph for efficient storage.'
  },
  {
    label: 'Mutate',
    color: '#f59e42',
    tooltip: '🌀 Mutate: Apply random mutation to current glyph.',
    endpoint: '/api/glyph/mutate',
    method: 'POST',
    body: (glyph: any) => ({ glyph, format: 'svg' }),
    assistant: 'Mutate will introduce random changes to the glyph, exploring new forms.'
  },
  {
    label: 'Reset',
    color: '#ef4444',
    tooltip: '🔁 Reset: Revert vault state (not implemented).',
    endpoint: '/api/vault/reset',
    method: 'POST',
    body: () => ({}),
    assistant: 'Reset will revert the vault to its previous state. (Coming soon!)'
  },
];

export default function RitualButtons({ glyph, setGlyphSvg }: RitualButtonsProps) {
  const [hovered, setHovered] = useState<string | null>(null);

  const handleClick = async (ritual: any) => {
    if (ritual.label === 'Reset') {
      alert('Reset ritual not yet implemented.');
      return;
    }
    const body = ritual.body(glyph);
    const res = await fetch(`http://localhost:8000${ritual.endpoint}`, {
      method: ritual.method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (ritual.label === 'Compress') {
      const data = await res.json();
      alert('Compressed JSON: ' + data.compressed);
    } else {
      const svg = await res.text();
      setGlyphSvg(svg);
    }
  };

  const hoveredRitual = rituals.find(r => r.label === hovered);

  return (
    <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 0, margin: '24px 0' }}>
      {hoveredRitual && (
        <div style={{
          position: 'absolute',
          top: -56,
          left: 0,
          background: '#fff',
          border: '1.5px solid #0070f3',
          borderRadius: 10,
          boxShadow: '0 2px 12px rgba(0,0,0,0.10)',
          padding: '12px 18px',
          color: '#222',
          fontSize: 15,
          zIndex: 10,
          minWidth: 220,
          maxWidth: 320,
        }}>
          <span style={{ fontWeight: 700, color: '#0070f3' }}>Gene Suggests:</span><br />
          {hoveredRitual.assistant}
        </div>
      )}
      <div style={{ display: 'flex', gap: 16 }}>
        {rituals.map((r) => (
          <button
            key={r.label}
            onClick={() => handleClick(r)}
            title={r.tooltip}
            onMouseEnter={() => setHovered(r.label)}
            onMouseLeave={() => setHovered(null)}
            style={{
              background: r.color,
              color: '#fff',
              border: 'none',
              borderRadius: 8,
              padding: '10px 22px',
              fontWeight: 600,
              fontSize: 16,
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
              transition: 'background 0.2s',
            }}
          >
            {r.label}
          </button>
        ))}
      </div>
    </div>
  );
} 