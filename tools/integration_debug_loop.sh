#!/bin/bash
# integration_debug_loop.sh
# Codex Ritual: Automated integration debug loop for frontend-backend systems

set -e

API_URL="http://127.0.0.1:8000/api/gene/rituals_with_glyphs"
FRONTEND_ENV="frontend/.env.local"
NEXT_CONFIG="frontend/next.config.js"
LOG_FILE="/tmp/codex.debug.log"

function log() {
  echo -e "\033[1;34m[Codex Debug]\033[0m $1"
  echo "[Codex Debug] $1" >> "$LOG_FILE"
}

log "--- Codex Integration Debug Ritual ---"
log "1. Checking backend reachability with curl..."
curl -i "$API_URL" | tee -a "$LOG_FILE"

log "2. Checking frontend .env.local for API base URL..."
if [ -f "$FRONTEND_ENV" ]; then
  cat "$FRONTEND_ENV" | grep NEXT_PUBLIC_API_BASE_URL | tee -a "$LOG_FILE"
else
  log "[WARN] $FRONTEND_ENV not found!"
fi

log "3. Checking Next.js proxy config (if present)..."
if [ -f "$NEXT_CONFIG" ]; then
  grep 'rewrites' "$NEXT_CONFIG" | tee -a "$LOG_FILE"
else
  log "[INFO] $NEXT_CONFIG not found (proxy not set)"
fi

log "4. Testing API endpoint with node-fetch (if available)..."
if command -v node > /dev/null && npm list node-fetch > /dev/null 2>&1; then
  node -e "const fetch = require('node-fetch'); fetch('$API_URL').then(r => r.json()).then(j => console.log(j)).catch(e => console.error(e));" | tee -a "$LOG_FILE"
else
  log "[INFO] node-fetch not available, skipping Node.js fetch test."
fi

log "5. Suggest: Open browser dev tools → Network tab → refresh Rituals page. Look for CORS or network errors."
log "6. Suggest: Use Postman to test $API_URL for valid JSON."

log "--- Ritual complete. Review $LOG_FILE for details. ---" 