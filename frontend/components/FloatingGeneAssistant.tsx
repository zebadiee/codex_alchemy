import { useState, useRef } from 'react';

export default function FloatingGeneAssistant() {
  const [pos, setPos] = useState({ x: 40, y: 80 });
  const [dragging, setDragging] = useState(false);
  const offset = useRef({ x: 0, y: 0 });

  const onMouseDown = (e: React.MouseEvent) => {
    setDragging(true);
    offset.current = {
      x: e.clientX - pos.x,
      y: e.clientY - pos.y,
    };
    document.body.style.userSelect = 'none';
  };

  const onMouseMove = (e: MouseEvent) => {
    if (dragging) {
      setPos({
        x: e.clientX - offset.current.x,
        y: e.clientY - offset.current.y,
      });
    }
  };

  const onMouseUp = () => {
    setDragging(false);
    document.body.style.userSelect = '';
  };

  // Attach/detach listeners
  if (typeof window !== 'undefined') {
    window.onmousemove = dragging ? onMouseMove : null;
    window.onmouseup = dragging ? onMouseUp : null;
  }

  return (
    <div
      style={{
        position: 'fixed',
        left: pos.x,
        top: pos.y,
        zIndex: 9999,
        background: 'rgba(255,255,255,0.95)',
        border: '2px solid #0070f3',
        borderRadius: 12,
        boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
        width: 260,
        padding: 18,
        cursor: dragging ? 'grabbing' : 'grab',
        transition: 'box-shadow 0.2s',
      }}
      onMouseDown={onMouseDown}
    >
      <div style={{ fontWeight: 700, fontSize: 18, color: '#0070f3', marginBottom: 8 }}>
        🧬 Gene Assistant
      </div>
      <div style={{ fontSize: 15, color: '#333' }}>
        Hi! I'm Gene, your symbolic AI assistant.<br />
        <span style={{ color: '#888', fontSize: 13 }}>
          (Drag me anywhere. More features coming soon!)
        </span>
      </div>
    </div>
  );
} 