#!/usr/bin/env python3
"""
Unified CLI for Codex Alchemy + A0 Integration
Provides commands to work with both systems seamlessly
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.bridge_a0 import a0_bridge
except ImportError:
    print("Warning: A0 bridge not available")
    a0_bridge = None

class UnifiedCLI:
    def __init__(self):
        self.codex_path = Path(__file__).parent
        self.a0_path = self.codex_path / "a0"
        
    def status(self):
        """Show status of both systems"""
        print("🔮 Codex Alchemy + A0 Unified System")
        print("=" * 50)
        
        # Codex Alchemy status
        print("\n📚 Codex Alchemy:")
        print(f"  Path: {self.codex_path}")
        print(f"  Database: {'✅' if (self.codex_path / 'spiral_codex.db').exists() else '❌'}")
        print(f"  Vault: {'✅' if (self.codex_path / 'vault').exists() else '❌'}")
        print(f"  Frontend: {'✅' if (self.codex_path / 'frontend').exists() else '❌'}")
        print(f"  Backend: {'✅' if (self.codex_path / 'backend').exists() else '❌'}")
        
        # A0 status
        print("\n🤖 A0 System:")
        if a0_bridge and a0_bridge.is_a0_available():
            print(f"  Path: {self.a0_path}")
            print(f"  Available: ✅")
            print(f"  Agents: {len(a0_bridge.get_a0_agents())}")
            print(f"  Spells: {len(a0_bridge.get_a0_spells())}")
            print(f"  Lineage: {'✅' if a0_bridge.get_a0_lineage() else '❌'}")
        else:
            print(f"  Available: ❌")
            print(f"  Path: {self.a0_path}")
        
        # Unified status
        print("\n🔗 Integration:")
        if a0_bridge and a0_bridge.is_a0_available():
            merged = a0_bridge.merge_vaults()
            print(f"  Total Spells: {merged['merged']['total_spells']}")
            print(f"  Total Glyphs: {merged['merged']['total_glyphs']}")
            print(f"  Systems: {' + '.join(merged['merged']['systems'])}")
        else:
            print("  A0 not available for integration")
    
    def sync_vaults(self):
        """Sync vaults between a0 and Codex Alchemy"""
        print("🔗 Syncing vaults between a0 and Codex Alchemy...")
        
        try:
            # Try API first
            response = requests.get("http://localhost:8000/api/sync/vault", timeout=10)
            if response.status_code == 200:
                result = response.json()
                print("✅ Sync completed via API")
                data = result.get("data", {})
                print(f"  Glyphs: {data.get('glyphs', 0)}")
                print(f"  Rituals: {data.get('rituals', 0)}")
                print(f"  Spells: {data.get('spells', 0)}")
                print(f"  Agents: {data.get('agents', 0)}")
                print(f"  A0 Saved: {'✅' if data.get('a0_saved') else '❌'}")
                print(f"  Codex Saved: {'✅' if data.get('codex_saved') else '❌'}")
            else:
                print(f"❌ API sync failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("⚠️  Backend not running, attempting direct sync...")
            try:
                from backend.sync.vault_sync import sync_vaults
                result = sync_vaults()
                print("✅ Direct sync completed")
                print(f"  Glyphs: {result.get('glyphs', 0)}")
                print(f"  Rituals: {result.get('rituals', 0)}")
                print(f"  Spells: {result.get('spells', 0)}")
                print(f"  Agents: {result.get('agents', 0)}")
                return True
            except Exception as e:
                print(f"❌ Direct sync failed: {e}")
                return False
        
        return True
    
    def sync_status(self):
        """Show sync status"""
        print("📊 Sync Status:")
        print("=" * 30)
        
        try:
            response = requests.get("http://localhost:8000/api/sync/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                print(f"Status: {status.get('status', 'unknown')}")
                print(f"Vaults:")
                print(f"  A0: {'✅' if status.get('vaults', {}).get('a0') else '❌'}")
                print(f"  Codex: {'✅' if status.get('vaults', {}).get('codex') else '❌'}")
                print(f"Last Sync: {status.get('last_sync', 'Never')}")
                print(f"Log File: {status.get('log_file', 'N/A')}")
            else:
                print("❌ Could not fetch sync status")
        except requests.exceptions.RequestException:
            print("⚠️  Backend not running")
    
    def list_agents(self):
        """List available agents from both systems"""
        print("🤖 Available Agents:")
        print("=" * 30)
        
        if a0_bridge and a0_bridge.is_a0_available():
            agents = a0_bridge.get_a0_agents()
            print(f"\nA0 Agents ({len(agents)}):")
            for agent in agents:
                print(f"  • {agent}")
        else:
            print("\nA0 Agents: Not available")
        
        # Codex Alchemy agents (if any)
        codex_agents = []
        agent_dir = self.codex_path / "agent"
        if agent_dir.exists():
            for file in agent_dir.glob("*.py"):
                if not file.name.startswith("__"):
                    codex_agents.append(file.stem)
        
        print(f"\nCodex Alchemy Agents ({len(codex_agents)}):")
        for agent in codex_agents:
            print(f"  • {agent}")
    
    def list_spells(self):
        """List spells from both systems"""
        print("✨ Available Spells:")
        print("=" * 30)
        
        if a0_bridge and a0_bridge.is_a0_available():
            spells = a0_bridge.get_a0_spells()
            print(f"\nA0 Spells ({len(spells)}):")
            for spell in spells:
                print(f"  • {spell.get('file', 'Unknown')}")
                if spell.get('name'):
                    print(f"    Name: {spell['name']}")
        else:
            print("\nA0 Spells: Not available")
        
        # Codex Alchemy spells/rituals
        codex_vault = self.codex_path / "codex_vault_backup.json"
        if codex_vault.exists():
            try:
                with open(codex_vault, 'r') as f:
                    data = json.load(f)
                    rituals = data.get("RecoveredRitual", [])
                    print(f"\nCodex Alchemy Rituals ({len(rituals)}):")
                    for ritual in rituals:
                        name = ritual.get('name', 'Unknown')
                        print(f"  • {name}")
            except Exception as e:
                print(f"\nCodex Alchemy Rituals: Error loading - {e}")
    
    def start_backend(self):
        """Start the FastAPI backend"""
        print("🚀 Starting Codex Alchemy Backend...")
        os.chdir(self.codex_path)
        os.system("uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
    
    def start_frontend(self):
        """Start the Next.js frontend"""
        print("🎨 Starting Codex Alchemy Frontend...")
        frontend_path = self.codex_path / "frontend"
        if frontend_path.exists():
            os.chdir(frontend_path)
            os.system("npm run dev")
        else:
            print("❌ Frontend directory not found")
    
    def start_a0(self):
        """Start A0 system if available"""
        if a0_bridge and a0_bridge.is_a0_available():
            print("🤖 Starting A0 System...")
            os.chdir(self.a0_path)
            if (self.a0_path / "start_a0.sh").exists():
                os.system("./start_a0.sh")
            else:
                print("❌ A0 start script not found")
        else:
            print("❌ A0 system not available")
    
    def migrate_data(self):
        """Migrate data between systems"""
        print("🔄 Migrating data...")
        
        if a0_bridge and a0_bridge.is_a0_available():
            # This would implement data migration logic
            print("✅ A0 bridge available for migration")
            merged = a0_bridge.merge_vaults()
            print(f"📊 Found {merged['merged']['total_spells']} spells and {merged['merged']['total_glyphs']} glyphs")
        else:
            print("❌ A0 not available for migration")
    
    def test_integration(self):
        """Test the integration between systems"""
        print("🧪 Testing Integration...")
        
        # Test A0 bridge
        if a0_bridge:
            print(f"✅ A0 Bridge: {'Available' if a0_bridge.is_a0_available() else 'Not Available'}")
            if a0_bridge.is_a0_available():
                print(f"  Agents: {len(a0_bridge.get_a0_agents())}")
                print(f"  Spells: {len(a0_bridge.get_a0_spells())}")
        else:
            print("❌ A0 Bridge: Not loaded")
        
        # Test Codex Alchemy
        print(f"✅ Codex Alchemy: Available")
        print(f"  Database: {'✅' if (self.codex_path / 'spiral_codex.db').exists() else '❌'}")
        print(f"  Backend: {'✅' if (self.codex_path / 'backend').exists() else '❌'}")
        print(f"  Frontend: {'✅' if (self.codex_path / 'frontend').exists() else '❌'}")

    def refine_script_cli(self, script_path):
        with open(script_path) as f:
            script = f.read()
        rating = int(input("Rating (1–5): "))
        comments = input("Feedback: ")

        r = requests.post("http://localhost:8000/api/refine-script", json={
            "script": script,
            "feedback": {"rating": rating, "comments": comments}
        })
        print("\n--- Refined Output ---\n")
        print(r.json()["refined_script"])

    def dream_loop(self):
        """Execute the dream loop ritual for symbolic evolution"""
        print("🌙 Initiating Dream Loop Ritual...")
        print("=" * 40)
        
        try:
            # Try API first
            response = requests.post("http://localhost:8000/api/dream-loop", timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Dream loop completed successfully!")
                print(f"📊 {result.get('summary', 'Glyphs evolved')}")
                print(f"⏱️  Duration: {result.get('duration', 'Unknown')}")
            else:
                print(f"❌ API error: {response.status_code}")
        except requests.exceptions.RequestException:
            print("🌐 API unavailable, running local dream loop...")
            # Fallback to local execution
            try:
                from codex_alchemy.rituals.evolve import evolve_glyphs
                from codex_alchemy.vault import restore, preserve
                
                glyphs = restore("default")
                if glyphs:
                    evolved = evolve_glyphs(glyphs)
                    preserve("evolved", evolved)
                    print(f"✅ Local dream loop completed! {len(evolved)} glyphs evolved.")
                else:
                    print("❌ No glyphs found in 'default' sigil")
            except Exception as e:
                print(f"❌ Local dream loop failed: {e}")

    def gene_assist(self, prompt=None):
        """Interact with Gene Assistant"""
        if not prompt:
            prompt = input("🤖 Ask Gene: ")
        
        print(f"🤖 Gene Assistant: {prompt}")
        print("=" * 40)
        
        try:
            response = requests.post("http://localhost:8000/api/assistant/respond", 
                                   json={"prompt": prompt, "context": {}}, 
                                   timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"💬 {result['response']}")
                if result.get('ritual_hint'):
                    print(f"💡 {result['ritual_hint']}")
                if result.get('suggestions'):
                    print(f"🔗 Suggestions: {', '.join(result['suggestions'])}")
            else:
                print(f"❌ API error: {response.status_code}")
        except requests.exceptions.RequestException:
            print("🌐 Gene is offline. Here are some helpful commands:")
            print("• python unified_cli.py dream-loop")
            print("• codex-alchemy vault diff default evolved")
            print("• python unified_cli.py sync-status")

    def gene_status(self):
        """Check Gene Assistant status"""
        print("🤖 Gene Assistant Status")
        print("=" * 30)
        
        try:
            response = requests.get("http://localhost:8000/api/assistant/status", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"📊 Status: {result['status']}")
                print(f"💬 Recent interactions: {result['recent_interactions']}")
                if result.get('last_interaction'):
                    print(f"🕐 Last interaction: {result['last_interaction']['timestamp']}")
            else:
                print(f"❌ API error: {response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ Gene Assistant is offline")

def main():
    parser = argparse.ArgumentParser(description="Unified CLI for Codex Alchemy + A0")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # List commands
    subparsers.add_parser('agents', help='List available agents')
    subparsers.add_parser('spells', help='List available spells')
    
    # Sync commands
    subparsers.add_parser('sync', help='Sync vaults between a0 and Codex Alchemy')
    subparsers.add_parser('sync-status', help='Show sync status')
    
    # Start commands
    subparsers.add_parser('backend', help='Start FastAPI backend')
    subparsers.add_parser('frontend', help='Start Next.js frontend')
    subparsers.add_parser('a0', help='Start A0 system')
    
    # Utility commands
    subparsers.add_parser('migrate', help='Migrate data between systems')
    subparsers.add_parser('test', help='Test integration')
    subparsers.add_parser('refine', help='Refine a script via feedback (usage: refine path/to/script.py)')
    subparsers.add_parser('dream-loop', help='Execute the dream loop ritual for symbolic evolution')
    gene_assist_parser = subparsers.add_parser('gene-assist', help='Interact with Gene Assistant')
    gene_assist_parser.add_argument('prompt', nargs='*', help='Prompt for Gene Assistant')
    subparsers.add_parser('gene-status', help='Check Gene Assistant status')
    
    args = parser.parse_args()
    
    cli = UnifiedCLI()
    
    if args.command == 'status':
        cli.status()
    elif args.command == 'agents':
        cli.list_agents()
    elif args.command == 'spells':
        cli.list_spells()
    elif args.command == 'sync':
        cli.sync_vaults()
    elif args.command == 'sync-status':
        cli.sync_status()
    elif args.command == 'backend':
        cli.start_backend()
    elif args.command == 'frontend':
        cli.start_frontend()
    elif args.command == 'a0':
        cli.start_a0()
    elif args.command == 'migrate':
        cli.migrate_data()
    elif args.command == 'test':
        cli.test_integration()
    elif args.command == 'refine':
        if len(sys.argv) < 3:
            print("Usage: python unified_cli.py refine path/to/script.py")
            sys.exit(1)
        cli.refine_script_cli(sys.argv[2])
    elif args.command == 'dream-loop':
        cli.dream_loop()
    elif args.command == 'gene-assist':
        if args.prompt:
            prompt = ' '.join(args.prompt)
            cli.gene_assist(prompt)
        else:
            cli.gene_assist()
    elif args.command == 'gene-status':
        cli.gene_status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 