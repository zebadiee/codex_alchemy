"""
Sync API Routes
Provides endpoints for vault synchronization
"""

from fastapi import APIRouter, HTTPException
from backend.sync.vault_sync import sync_vaults, vault_sync
from typing import Dict, Any
import os
from pathlib import Path

router = APIRouter(prefix="/api/sync", tags=["Synchronization"])

@router.get("/vault")
async def vault_sync_route():
    """Trigger vault synchronization between a0 and Codex Alchemy"""
    try:
        result = sync_vaults()
        return {
            "status": "success",
            "message": "Vault synchronization completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@router.get("/status")
async def sync_status():
    """Get synchronization status and statistics"""
    try:
        # Check vault files
        vault_a0 = Path("a0/vault/vault.json")
        vault_codex = Path("codex_vault_backup.json")
        vault_codex_alt = Path("vault/ritual_log.jsonl")
        
        # Check log file
        log_path = Path("sync_logs/vault_sync.log")
        last_sync = None
        if log_path.exists():
            with open(log_path, "r") as f:
                lines = f.readlines()
                if lines:
                    last_sync = lines[-1].strip()
        
        return {
            "status": "ready",
            "vaults": {
                "a0": vault_a0.exists(),
                "codex": vault_codex.exists() or vault_codex_alt.exists()
            },
            "last_sync": last_sync,
            "log_file": str(log_path),
            "backup_dir": str(Path("sync_logs/backups"))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.get("/logs")
async def sync_logs(limit: int = 50):
    """Get recent synchronization logs"""
    try:
        log_path = Path("sync_logs/vault_sync.log")
        if not log_path.exists():
            return {"logs": [], "message": "No sync logs found"}
        
        with open(log_path, "r") as f:
            lines = f.readlines()
            recent_logs = lines[-limit:] if len(lines) > limit else lines
        
        return {
            "logs": [line.strip() for line in recent_logs],
            "total_entries": len(lines),
            "showing_last": len(recent_logs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log retrieval failed: {str(e)}")

@router.post("/auto-sync")
async def enable_auto_sync(interval_minutes: int = 5):
    """Enable automatic synchronization (placeholder for future implementation)"""
    return {
        "status": "configured",
        "message": f"Auto-sync configured for every {interval_minutes} minutes",
        "interval_minutes": interval_minutes,
        "note": "Auto-sync implementation coming in next iteration"
    } 