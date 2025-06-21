import json
from pathlib import Path
from datetime import datetime

VAULT_DIR = Path.home() / "codex_alchemy" / "vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

def log_ritual_event(mode: str, prompt: str, result: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "mode": mode,
        "prompt": prompt,
        "result": result,
    }
    log_file = VAULT_DIR / "ritual_log.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
