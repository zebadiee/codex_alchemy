#!/bin/bash
# Usage: ./run.sh
# This script installs dependencies and starts backend and frontend servers.

set -e

echo "[1/4] Installing backend dependencies..."
make install-backend

echo "[2/4] Installing frontend dependencies..."
make install-frontend

echo "[3/4] Installing CLI..."
make install-cli

echo "[4/4] Starting backend server in background..."
cd backend && uvicorn main:app --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3

# Health check for backend
if curl -s http://localhost:8000/docs > /dev/null; then
  echo "[OK] Backend is running at http://localhost:8000"
else
  echo "[ERROR] Backend did not start correctly. Check backend.log."
  exit 1
fi

echo "[5/5] Starting frontend server in foreground..."
cd frontend && npm run dev 