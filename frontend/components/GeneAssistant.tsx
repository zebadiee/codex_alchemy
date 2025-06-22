import React from 'react';

export default function GeneAssistant({ suggestions, onConfirm }) {
  return (
    <div style={{
      position: 'fixed',
      bottom: 24,
      right: 24,
      width: 320,
      background: '#0f172a',
      color: '#fff',
      padding: 16,
      borderRadius: 12,
      boxShadow: '0 6px 20px rgba(0,0,0,0.25)',
      zIndex: 9999
    }}>
      <h3 style={{ marginBottom: 12 }}>🧬 Gene's Suggestions</h3>
      {suggestions.length === 0 ? (
        <p style={{ fontStyle: 'italic', opacity: 0.7 }}>No active rituals yet...</p>
      ) : (
        suggestions.map((sug, idx) => (
          <div key={idx} style={{ marginBottom: 12, padding: 8, background: '#1e293b', borderRadius: 8 }}>
            <strong>{sug.title}</strong>
            <p style={{ fontSize: 13 }}>{sug.message}</p>
            <button onClick={() => onConfirm(sug.ritual)} style={{
              background: '#10b981',
              border: 'none',
              color: '#fff',
              padding: '6px 12px',
              borderRadius: 6,
              marginTop: 6,
              cursor: 'pointer'
            }}>
              ✨ Confirm: {sug.ritual}
            </button>
          </div>
        ))
      )}
    </div>
  );
} 