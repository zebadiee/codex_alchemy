.PHONY: backend frontend install-backend install-frontend install-cli

backend:
	PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

install-backend:
	pip install -e .[dev]

install-frontend:
	cd frontend && npm install

install-cli:
	pip install -e . 