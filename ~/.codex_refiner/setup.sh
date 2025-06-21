#!/bin/bash
set -e

echo "🔮 Installing Codex Refiner Shadow Add-On..."

# Create core refinement module
cat > ~/.codex_refiner/core/refine_paper.py <<'PY'
import json
import os
from datetime import datetime
from pathlib import Path

def refine_paper(json_payload: str) -> str:
    """Apply symbolic refinement to research paper data"""
    try:
        data = json.loads(json_payload)
        refined = []
        
        for entry in data.get("results", []):
            paper = entry.get("summary", "")
            title = entry.get("title", "")
            
            # Apply symbolic refinement rules
            if "hallucination" in paper.lower() or "benchmark" in paper.lower():
                paper += "\n\n# 🔍 Codex Note: Validate against benchmark X / real dataset Y"
            
            if "2023" in paper or "2024" in paper:
                paper += "\n# 📅 Codex Note: Check for more recent developments"
            
            if "accuracy" in paper.lower() or "performance" in paper.lower():
                paper += "\n# ⚡ Codex Note: Consider computational efficiency trade-offs"
            
            # Add symbolic sigil
            sigil = f"🔮 [Codex-{datetime.now().strftime('%Y%m%d-%H%M%S')}]"
            paper = f"{sigil}\n{paper}"
            
            refined.append({
                "title": title,
                "refined_summary": paper,
                "refined_at": datetime.now().isoformat(),
                "sigil": sigil
            })
        
        return json.dumps({"refined_papers": refined}, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e), "original": json_payload})

def log_to_vault(refined_data: str):
    """Log refined data to symbolic vault"""
    vault_path = Path("~/.codex_refiner/vault.jsonl").expanduser()
    vault_path.parent.mkdir(exist_ok=True)
    
    with open(vault_path, "a") as f:
        f.write(f"{refined_data}\n")
PY

# Create passive interceptor
cat > ~/.codex_refiner/shadow/intercept.py <<'PY'
import re
import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
sys.path.append(str(Path("~/.codex_refiner/core").expanduser()))

from refine_paper import refine_paper, log_to_vault

class PaperHookHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("search_output.json"):
            print(f"🔍 Codex detected research output: {event.src_path}")
            
            try:
                with open(event.src_path) as f:
                    payload = f.read()
                
                refined = refine_paper(payload)
                log_to_vault(refined)
                
                # Write refined output
                refined_path = event.src_path.replace(".json", "_refined.json")
                with open(refined_path, "w") as out:
                    out.write(refined)
                
                print(f"✅ Codex refinement complete: {refined_path}")
                
            except Exception as e:
                print(f"❌ Codex refinement failed: {e}")

def start_interceptor():
    """Start the passive interceptor"""
    observer = Observer()
    observer.schedule(PaperHookHandler(), path="/tmp/findmypapers/", recursive=False)
    observer.start()
    
    print("🔮 Codex Refiner Shadow Add-On active")
    print("📁 Watching: /tmp/findmypapers/search_output.json")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Codex Refiner stopped")
    
    observer.join()

if __name__ == "__main__":
    start_interceptor()
PY

# Create manual refinement script
cat > ~/.codex_refiner/codex_refine.sh <<'SH'
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: codex_refine.sh <path_to_json_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.json}_refined.json"

echo "🔮 Codex Refiner processing: $INPUT_FILE"

python3 -c "
import sys
sys.path.append('$HOME/.codex_refiner/core')
from refine_paper import refine_paper, log_to_vault

with open('$INPUT_FILE') as f:
    payload = f.read()

refined = refine_paper(payload)
log_to_vault(refined)

with open('$OUTPUT_FILE', 'w') as f:
    f.write(refined)

print('✅ Refinement complete: $OUTPUT_FILE')
"

echo "📊 Refined output saved to: $OUTPUT_FILE"
SH

# Make scripts executable
chmod +x ~/.codex_refiner/codex_refine.sh

# Create symbolic vault
mkdir -p ~/.codex_refiner/vault
touch ~/.codex_refiner/vault.jsonl

# Install required dependencies
pip3 install watchdog

echo "✅ Codex Refiner Shadow Add-On installed successfully!"
echo ""
echo "🔧 Available commands:"
echo "  • codex_refine.sh <file.json> - Manual refinement"
echo "  • python3 ~/.codex_refiner/shadow/intercept.py - Start passive interceptor"
echo ""
echo "📁 Files created:"
echo "  • ~/.codex_refiner/core/refine_paper.py"
echo "  • ~/.codex_refiner/shadow/intercept.py"
echo "  • ~/.codex_refiner/codex_refine.sh"
echo "  • ~/.codex_refiner/vault.jsonl"
echo ""
echo "🔮 Ready for undetectable research enhancement!" 