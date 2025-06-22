import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ padding: 32, fontFamily: 'sans-serif' }}>
      <h1>🧬 The Ai Catalogue</h1>
      <p>Welcome to your next-gen symbolic glyph engine and Codex Alchemy project.</p>
      <ul style={{ marginTop: 24 }}>
        <li>
          <Link href="/glyph-viewer">
            <a style={{ fontSize: 18, color: '#0070f3' }}>🔎 Glyph Viewer</a>
          </Link>
        </li>
      </ul>
      <p style={{ marginTop: 40, color: '#888' }}>
        Powered by FastAPI, Next.js, and Codex Alchemy.
      </p>
    </div>
  );
} 