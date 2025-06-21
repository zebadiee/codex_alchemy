#!/usr/bin/env python3
"""
Codex Refiner CLI Control Layer
Provides comprehensive control over the undetectable research enhancement system
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class CodexRefinerCLI:
    def __init__(self):
        self.home = Path.home()
        self.codex_dir = self.home / ".codex_refiner"
        self.vault_path = self.codex_dir / "vault.jsonl"
        self.core_path = self.codex_dir / "core"
        
    def status(self):
        """Show Codex Refiner system status"""
        print("🔮 Codex Refiner Shadow Add-On Status")
        print("=" * 50)
        
        # Check installation
        if self.codex_dir.exists():
            print(f"✅ Installation: {self.codex_dir}")
        else:
            print("❌ Installation: Not found")
            return
        
        # Check core files
        core_files = ["refine_paper.py", "codex_refine.sh"]
        for file in core_files:
            path = self.codex_dir / file if file.endswith('.sh') else self.core_path / file
            if path.exists():
                print(f"✅ {file}: {path}")
            else:
                print(f"❌ {file}: Missing")
        
        # Check vault
        if self.vault_path.exists():
            with open(self.vault_path) as f:
                lines = f.readlines()
            print(f"✅ Vault: {len(lines)} entries")
        else:
            print("❌ Vault: Not found")
        
        # Check dependencies
        try:
            import watchdog
            print("✅ Dependencies: watchdog installed")
        except ImportError:
            print("❌ Dependencies: watchdog missing (pip install watchdog)")
    
    def refine(self, input_file: str):
        """Refine a research file"""
        if not Path(input_file).exists():
            print(f"❌ File not found: {input_file}")
            return
        
        print(f"🔮 Refining: {input_file}")
        
        try:
            result = subprocess.run([
                str(self.codex_dir / "codex_refine.sh"),
                input_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Refinement complete")
                print(result.stdout)
            else:
                print("❌ Refinement failed")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def vault(self, action: str = "list"):
        """Manage the symbolic vault"""
        if not self.vault_path.exists():
            print("❌ Vault not found")
            return
        
        if action == "list":
            print("🔮 Symbolic Vault Contents")
            print("=" * 50)
            
            with open(self.vault_path) as f:
                for i, line in enumerate(f, 1):
                    try:
                        data = json.loads(line.strip())
                        papers = data.get("refined_papers", [])
                        for paper in papers:
                            print(f"{i}. {paper.get('title', 'Unknown')}")
                            print(f"   Sigil: {paper.get('sigil', 'None')}")
                            print(f"   Date: {paper.get('refined_at', 'Unknown')}")
                            print()
                    except json.JSONDecodeError:
                        print(f"{i}. Invalid JSON entry")
                        print()
        
        elif action == "stats":
            print("📊 Vault Statistics")
            print("=" * 30)
            
            total_entries = 0
            total_papers = 0
            sigils = set()
            dates = set()
            
            with open(self.vault_path) as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        total_entries += 1
                        papers = data.get("refined_papers", [])
                        total_papers += len(papers)
                        
                        for paper in papers:
                            sigils.add(paper.get('sigil', ''))
                            date = paper.get('refined_at', '').split('T')[0]
                            if date:
                                dates.add(date)
                    except json.JSONDecodeError:
                        continue
            
            print(f"Total Vault Entries: {total_entries}")
            print(f"Total Refined Papers: {total_papers}")
            print(f"Unique Sigils: {len(sigils)}")
            print(f"Refinement Days: {len(dates)}")
        
        elif action == "clear":
            confirm = input("⚠️  Clear entire vault? (yes/no): ")
            if confirm.lower() == "yes":
                self.vault_path.write_text("")
                print("✅ Vault cleared")
            else:
                print("❌ Vault clear cancelled")
    
    def watch(self, directory: str = "/tmp/findmypapers"):
        """Start the passive interceptor"""
        watch_path = Path(directory)
        if not watch_path.exists():
            print(f"📁 Creating watch directory: {watch_path}")
            watch_path.mkdir(parents=True, exist_ok=True)
        
        print(f"🔮 Starting passive interceptor...")
        print(f"📁 Watching: {watch_path}")
        print("Press Ctrl+C to stop")
        
        try:
            # Start the interceptor
            interceptor_path = self.codex_dir / "shadow" / "intercept.py"
            if interceptor_path.exists():
                subprocess.run([sys.executable, str(interceptor_path)])
            else:
                print("❌ Interceptor not found. Run setup first.")
        except KeyboardInterrupt:
            print("\n🛑 Interceptor stopped")
    
    def test(self):
        """Test the refinement system"""
        print("🧪 Testing Codex Refiner System")
        print("=" * 40)
        
        # Create test data
        test_data = {
            "results": [
                {
                    "title": "Test Research Paper",
                    "summary": "This is a test paper with hallucination detection and 2023 benchmarks. Performance analysis shows good accuracy."
                }
            ]
        }
        
        test_file = "test_refiner.json"
        with open(test_file, "w") as f:
            json.dump(test_data, f, indent=2)
        
        print(f"📝 Created test file: {test_file}")
        
        # Test refinement
        self.refine(test_file)
        
        # Check output
        refined_file = "test_refiner_refined.json"
        if Path(refined_file).exists():
            print(f"✅ Refined output: {refined_file}")
            with open(refined_file) as f:
                data = json.load(f)
                papers = data.get("refined_papers", [])
                if papers:
                    print(f"📊 Refined {len(papers)} papers")
                    for paper in papers:
                        print(f"   • {paper.get('title')}")
                        print(f"   • Sigil: {paper.get('sigil')}")
        else:
            print("❌ Refined output not found")
        
        # Cleanup
        for file in [test_file, refined_file]:
            if Path(file).exists():
                Path(file).unlink()
                print(f"🧹 Cleaned up: {file}")

def main():
    parser = argparse.ArgumentParser(description="Codex Refiner CLI Control Layer")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Refine command
    refine_parser = subparsers.add_parser('refine', help='Refine a research file')
    refine_parser.add_argument('file', help='Path to JSON file to refine')
    
    # Vault commands
    vault_parser = subparsers.add_parser('vault', help='Manage symbolic vault')
    vault_parser.add_argument('action', choices=['list', 'stats', 'clear'], 
                             default='list', help='Vault action')
    
    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Start passive interceptor')
    watch_parser.add_argument('--dir', default='/tmp/findmypapers', 
                             help='Directory to watch')
    
    # Test command
    subparsers.add_parser('test', help='Test the refinement system')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CodexRefinerCLI()
    
    if args.command == 'status':
        cli.status()
    elif args.command == 'refine':
        cli.refine(args.file)
    elif args.command == 'vault':
        cli.vault(args.action)
    elif args.command == 'watch':
        cli.watch(args.dir)
    elif args.command == 'test':
        cli.test()

if __name__ == "__main__":
    main() 