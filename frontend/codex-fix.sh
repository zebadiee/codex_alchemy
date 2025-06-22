#!/bin/bash

# Always safe on macOS
cd "$(dirname "$0")" || exit 1
mkdir -p src/app

cat <<'EOF' > src/app/page.tsx
'use client';

export default function Home() {
  return (
    <main>
      <h1>Hello, Codex Alchemy</h1>
    </main>
  );
}
EOF

echo "✅ page.tsx updated."

# Kill anything already using port 3000
lsof -ti :3000 | xargs kill -9 2>/dev/null

echo "🚀 Starting dev server..."
npm run dev

