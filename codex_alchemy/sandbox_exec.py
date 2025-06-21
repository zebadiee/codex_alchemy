#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

VENV_DIR = Path("codex_sandbox")
LOGFILE = Path("sandbox.log")

def log(message):
    print(f"[sandbox] {message}")
    with open(LOGFILE, "a") as logf:
        logf.write(f"[sandbox] {message}\n")

def ensure_venv():
    if not VENV_DIR.exists():
        log("Creating sandbox virtual environment...")
        subprocess.run(["python3", "-m", "venv", str(VENV_DIR)], check=True)
        log("Sandbox venv created.")
    else:
        log("Sandbox venv already exists.")

def run_in_venv(command_args):
    venv_python = VENV_DIR / "bin" / "python"
    if not venv_python.exists():
        log("Error: Python binary in venv not found.")
        sys.exit(1)

    full_command = [str(venv_python)] + command_args
    log(f"Executing: {' '.join(full_command)}")
    result = subprocess.run(full_command, capture_output=True, text=True)

    if result.stdout:
        log("[stdout]")
        log(result.stdout)
    if result.stderr:
        log("[stderr]")
        log(result.stderr)

    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sandbox_exec.py <command> [args...]")
        sys.exit(1)

    ensure_venv()
    exit_code = run_in_venv(sys.argv[1:])
    sys.exit(exit_code)

