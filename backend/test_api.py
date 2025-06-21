import pytest
from httpx import AsyncClient
from backend.main import app
import sqlite3
import os

LOG_DB = "test_results.db"

def log_result(test_name, status, message=None):
    conn = sqlite3.connect(LOG_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS test_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT,
            status TEXT,
            message TEXT
        )
    """)
    c.execute("INSERT INTO test_log (test_name, status, message) VALUES (?, ?, ?)", (test_name, status, message))
    conn.commit()
    conn.close()

@pytest.mark.asyncio
async def test_get_rituals():
    try:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/gene/rituals")
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        log_result("test_get_rituals", "PASS")
    except Exception as e:
        log_result("test_get_rituals", "FAIL", str(e))
        raise

@pytest.mark.asyncio
async def test_post_ritual():
    try:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = {"name": "Automated Ritual", "description": "Created by test"}
            response = await ac.post("/api/gene/rituals", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "created"
            assert data["ritual"]["name"] == "Automated Ritual"
        log_result("test_post_ritual", "PASS")
    except Exception as e:
        log_result("test_post_ritual", "FAIL", str(e))
        raise 