#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.expanduser("~/codex_alchemy"))
import argparse
from agent.tools.token_guard import reduce_prompt
from pathlib import Path
from datetime import datetime
import json

CONFIG_PATH = Path.home() / "codex_alchemy" / "agent_config.json"

def gene_process(instruction):
    compressed = reduce_prompt(instruction, verbose=True)
    return f"🔮 {compressed} ✨"

def log_to_ledger(gene_result, mode='evolve'):
    ledger_path = Path.home() / 'codex_alchemy' / '.vault' / 'ledger.jsonl'
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'mode': mode,
        'result': gene_result
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, 'a') as f:
        f.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Gene with mode support')
    parser.add_argument('instruction', type=str, help='Instruction for Gene')
    parser.add_argument('--mode', choices=['evolve', 'reflect', 'dream'], default='evolve', help='Operation mode')
    args = parser.parse_args()

    result = gene_process(args.instruction)
    log_to_ledger(result, mode=args.mode)

    print(f"\n💭 Mode: {args.mode.upper()}")
    print(result)
