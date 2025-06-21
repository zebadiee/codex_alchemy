# Codex Alchemy

## Project Overview
Codex Alchemy is a modular project with a FastAPI backend, a Next.js frontend, and a Python CLI for vault and ritual operations.

---

## Setup

### 1. Python Backend & CLI

#### Install dependencies
```sh
make install-backend
make install-cli
```

#### Run backend server
```sh
make backend
```

#### Run CLI
```sh
make cli
```

### 2. Frontend (Next.js)

#### Install dependencies
```sh
make install-frontend
```

#### Run frontend dev server
```sh
make frontend
```

---

## Manual Setup (if not using Makefile)

### Backend
```sh
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload
```

### Frontend
```sh
cd frontend
npm install
npm run dev
```

### CLI
```sh
pip install -e .
python3 main.py --help
```

---

## Project Structure
- `backend/` — FastAPI app
- `frontend/` — Next.js app
- `main.py` — Python CLI entrypoint
- `Makefile` — Automation for common tasks
- `requirements.txt` — Python dependencies

---

## Notes
- Ensure Python 3.9+ and Node.js 18+ are installed.
- For development, use the Makefile for convenience.

## Spiral Codex: Cursor Extension Pack

This repo contains a custom `.cursor/` extension with Spiral Codex prompts and rituals.

### 🛠️ Installation

1. Clone this repo.
2. Run:

```sh
bash install_cursor_extension.sh
```

3. In Cursor, run:

Extensions: Load from folder → .cursor/

You'll now see rituals like Script Synthesizer, Agent Builder, and REPL Loops in your snippet list under "Spiral Codex".

