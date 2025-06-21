.PHONY: backend frontend cli install-backend install-frontend install-cli backend-demo cli-demo

install-backend:
	pip install fastapi uvicorn

install-frontend:
	cd frontend && npm install

install-cli:
	pip install -e .

backend:
	cd backend && uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

cli:
	python3 main.py --help

backend-demo:
	@echo "Checking backend health..."
	@if curl -s http://localhost:8000/docs > /dev/null; then \
		echo "[OK] Backend is running at http://localhost:8000"; \
	else \
		echo "[ERROR] Backend is not running."; \
	fi

cli-demo:
	@echo "Showing CLI help and listing vault sigils..."
	python3 main.py --help
	python3 main.py vault list || true 