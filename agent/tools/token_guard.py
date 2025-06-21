import re
import sys
import json
from pathlib import Path
from datetime import datetime

MAX_LENGTH = 1024  # Optional limit to enforce truncation

# ✂️ Symbolic compression patterns (expandable)
substitutions = [
    (r"\bplease can you\b", ""),
    (r"\bcan you\b", ""),
    (r"\bcould you\b", ""),
    (r"\bi would like you to\b", ""),
    (r"\bi want you to\b", ""),
    (r"\bit is requested that you\b", ""),
    (r"\bthe goal is to\b", ""),
    (r"\bthis prompt asks you to\b", ""),
    (r"\byour task is to\b", ""),
    (r"\btask is\b", ""),
    (r"\bin order to\b", "to"),
    (r"\butilize\b", "use"),
    (r"\bwithin the context of\b", "in"),
    (r"\bthe following\b", ""),
    (r"\bmeaning within\b", "meaning in"),
    (r"\brecursive meaning\b", "recursion"),
    (r"\bsymbolic glyph lineage\b", "glyph lineage"),
    (r"\bvault system\b", "vault"),
    (r"\bsummarize and analyze\b", "analyze"),
]

def reduce_prompt(text, verbose=False):
    """Compresses prompt using pattern substitutions."""
    compressed = text
    for pattern, repl in substitutions:
        compressed = re.sub(pattern, repl, compressed, flags=re.IGNORECASE)

    compressed = re.sub(r"\s+", " ", compressed).strip()
    if len(compressed) > MAX_LENGTH:
        compressed = compressed[:MAX_LENGTH] + "..."

    if verbose:
        print("🔻 Prompt Compression Applied")
    return compressed

def log_to_ledger(result, mode='evolve'):
    """Logs result to symbolic ledger with timestamp and mode."""
    ledger_path = Path.home() / 'codex_alchemy' / '.vault' / 'ledger.jsonl'
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'mode': mode,
        'result': result
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def save_snapshot(original, compressed, mode='evolve'):
    """Saves before/after prompt snapshot for debugging/audit."""
    snap_path = Path.home() / 'codex_alchemy' / '.vault' / 'snapshots'
    snap_path.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"{mode}_snapshot_{ts}.json"
    with open(snap_path / filename, 'w') as f:
        json.dump({'original': original, 'compressed': compressed}, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 token_guard.py path/to/prompt.txt")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path, "r") as f:
            original = f.read()
        compressed = reduce_prompt(original, verbose=True)
        print("🪞 Compressed Prompt:\n", compressed)
    except Exception as e:
        print("❌ Error:", e)
