# sandbox_exec.py — symbolic CLI automation entrypoint

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sandbox_exec.py '<command>'")
        sys.exit(1)

    command = sys.argv[1]
    run_cmd(command)

