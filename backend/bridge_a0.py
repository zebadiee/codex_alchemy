"""
A0 Bridge Module
Enables seamless integration between codex_alchemy and a0 systems
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Add a0 to Python path
A0_PATH = Path(__file__).parent.parent / "a0"
if A0_PATH.exists():
    sys.path.insert(0, str(A0_PATH))

class A0Bridge:
    """Bridge between codex_alchemy and a0 systems"""
    
    def __init__(self):
        self.a0_path = A0_PATH
        self.a0_vault_path = self.a0_path / "vault"
        self.codex_vault_path = Path(__file__).parent.parent / "vault"
        
    def is_a0_available(self) -> bool:
        """Check if a0 system is available"""
        return self.a0_path.exists()
    
    def get_a0_agents(self) -> List[str]:
        """Get available a0 agents"""
        if not self.is_a0_available():
            return []
        
        agents = []
        for file in self.a0_path.glob("*.py"):
            if file.name.startswith("enforcer") or file.name == "agent.py":
                agents.append(file.stem)
        return agents
    
    def get_a0_spells(self) -> List[Dict[str, Any]]:
        """Get spells from a0 vault"""
        if not self.is_a0_available():
            return []
        
        spells_path = self.a0_vault_path / "spells"
        spells = []
        
        if spells_path.exists():
            for spell_file in spells_path.glob("*.json"):
                try:
                    with open(spell_file, 'r') as f:
                        spell_data = json.load(f)
                        spell_data['source'] = 'a0'
                        spell_data['file'] = spell_file.name
                        spells.append(spell_data)
                except Exception as e:
                    print(f"Error loading spell {spell_file}: {e}")
        
        return spells
    
    def get_a0_lineage(self) -> Dict[str, Any]:
        """Get lineage data from a0 vault"""
        if not self.is_a0_available():
            return {}
        
        lineage_file = self.a0_vault_path / "lineage.json"
        if lineage_file.exists():
            try:
                with open(lineage_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading lineage: {e}")
        
        return {}
    
    def import_a0_agent(self, agent_name: str):
        """Import an a0 agent dynamically"""
        if not self.is_a0_available():
            return None
        
        try:
            if agent_name == "enforcer_task_beast":
                from enforcer_task_beast import TaskBeast
                return TaskBeast()
            elif agent_name == "enforcer_token_breaker":
                from enforcer_token_breaker import TokenBreaker
                return TokenBreaker()
            elif agent_name == "agent":
                from agent import Agent
                return Agent()
            else:
                print(f"Unknown agent: {agent_name}")
                return None
        except ImportError as e:
            print(f"Error importing {agent_name}: {e}")
            return None
    
    def merge_vaults(self) -> Dict[str, Any]:
        """Merge codex_alchemy and a0 vaults"""
        merged = {
            "codex_alchemy": {},
            "a0": {},
            "merged": {}
        }
        
        # Get codex_alchemy vault data
        codex_vault_file = Path(__file__).parent.parent / "codex_vault_backup.json"
        if codex_vault_file.exists():
            try:
                with open(codex_vault_file, 'r') as f:
                    merged["codex_alchemy"] = json.load(f)
            except Exception as e:
                print(f"Error loading codex vault: {e}")
        
        # Get a0 vault data
        if self.is_a0_available():
            merged["a0"] = {
                "spells": self.get_a0_spells(),
                "lineage": self.get_a0_lineage()
            }
        
        # Create merged view
        merged["merged"] = {
            "total_spells": len(merged["a0"].get("spells", [])),
            "total_glyphs": len(merged["codex_alchemy"].get("RecoveredSigil", [])),
            "systems": ["codex_alchemy", "a0"]
        }
        
        return merged

# Global bridge instance
a0_bridge = A0Bridge() 