"""
Vault Synchronization Module
Handles bi-directional sync between a0 and Codex Alchemy vaults
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Vault paths
VAULT_A0 = Path("a0/vault/vault.json")
VAULT_CODEX = Path("codex_vault_backup.json")
VAULT_CODEX_ALT = Path("vault/ritual_log.jsonl")  # Alternative Codex vault location
LOG_PATH = Path("sync_logs/vault_sync.log")
BACKUP_DIR = Path("sync_logs/backups")

class VaultSync:
    """Handles synchronization between a0 and Codex Alchemy vaults"""
    
    def __init__(self):
        self.log_path = LOG_PATH
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(exist_ok=True)
        
    def load_vault(self, path: Path) -> Dict[str, Any]:
        """Load vault data from JSON file"""
        if not path.exists():
            self.log(f"Vault not found: {path}")
            return {"glyphs": [], "rituals": [], "spells": [], "agents": []}
        
        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.log(f"Loaded vault: {path} ({len(data.get('glyphs', []))} glyphs, {len(data.get('rituals', []))} rituals)")
                return data
        except Exception as e:
            self.log(f"Error loading vault {path}: {e}")
            return {"glyphs": [], "rituals": [], "spells": [], "agents": []}
    
    def load_codex_vault(self) -> Dict[str, Any]:
        """Load Codex vault from multiple possible locations"""
        # Try primary location first
        if VAULT_CODEX.exists():
            return self.load_vault(VAULT_CODEX)
        
        # Try alternative location
        if VAULT_CODEX_ALT.exists():
            try:
                # Handle JSONL format
                rituals = []
                with open(VAULT_CODEX_ALT, "r") as f:
                    for line in f:
                        if line.strip():
                            rituals.append(json.loads(line))
                return {"glyphs": [], "rituals": rituals, "spells": [], "agents": []}
            except Exception as e:
                self.log(f"Error loading JSONL vault: {e}")
        
        # Return empty vault if none found
        return {"glyphs": [], "rituals": [], "spells": [], "agents": []}
    
    def merge_entities(self, a: List[Dict], b: List[Dict], key: str = "id", timestamp: str = "updated_at") -> List[Dict]:
        """Merge entities with conflict resolution based on timestamps"""
        merged = {e.get(key, str(i)): e for i, e in enumerate(a)}
        
        for e in b:
            entity_key = e.get(key, str(len(merged)))
            if entity_key not in merged:
                merged[entity_key] = e
            else:
                # Conflict resolution: use newer timestamp
                existing = merged[entity_key]
                existing_time = existing.get(timestamp, "")
                new_time = e.get(timestamp, "")
                
                if new_time > existing_time:
                    merged[entity_key] = e
                    self.log(f"Updated entity {entity_key} (newer timestamp: {new_time})")
        
        return list(merged.values())
    
    def backup_vault(self, vault_path: Path, prefix: str = "") -> Path:
        """Create backup of vault before sync"""
        if not vault_path.exists():
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{prefix}vault_backup_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copy2(vault_path, backup_path)
            self.log(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            self.log(f"Backup failed: {e}")
            return None
    
    def save_vault(self, data: Dict[str, Any], path: Path) -> bool:
        """Save vault data to file"""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            self.log(f"Saved vault: {path}")
            return True
        except Exception as e:
            self.log(f"Error saving vault {path}: {e}")
            return False
    
    def log(self, message: str):
        """Log sync operations"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        # Ensure log directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.log_path, "a") as f:
            f.write(log_entry)
        
        print(f"🔗 {message}")
    
    def sync_vaults(self) -> Dict[str, Any]:
        """Main sync operation"""
        self.log("Starting vault synchronization...")
        
        # Load vaults
        vault_a0 = self.load_vault(VAULT_A0)
        vault_codex = self.load_codex_vault()
        
        # Create backups
        self.backup_vault(VAULT_A0, "a0_")
        self.backup_vault(VAULT_CODEX, "codex_")
        
        # Merge entities
        merged_glyphs = self.merge_entities(
            vault_a0.get("glyphs", []), 
            vault_codex.get("glyphs", [])
        )
        merged_rituals = self.merge_entities(
            vault_a0.get("rituals", []), 
            vault_codex.get("rituals", [])
        )
        merged_spells = self.merge_entities(
            vault_a0.get("spells", []), 
            vault_codex.get("spells", [])
        )
        merged_agents = self.merge_entities(
            vault_a0.get("agents", []), 
            vault_codex.get("agents", [])
        )
        
        # Create merged vault
        merged_vault = {
            "glyphs": merged_glyphs,
            "rituals": merged_rituals,
            "spells": merged_spells,
            "agents": merged_agents,
            "last_sync": datetime.now().isoformat(),
            "sync_version": "1.0"
        }
        
        # Save to both locations
        success_a0 = self.save_vault(merged_vault, VAULT_A0)
        success_codex = self.save_vault(merged_vault, VAULT_CODEX)
        
        # Log results
        result = {
            "glyphs": len(merged_glyphs),
            "rituals": len(merged_rituals),
            "spells": len(merged_spells),
            "agents": len(merged_agents),
            "a0_saved": success_a0,
            "codex_saved": success_codex,
            "timestamp": datetime.now().isoformat()
        }
        
        self.log(f"Sync completed: {result['glyphs']} glyphs, {result['rituals']} rituals, {result['spells']} spells, {result['agents']} agents")
        
        return result

# Global sync instance
vault_sync = VaultSync()

def sync_vaults() -> Dict[str, Any]:
    """Convenience function for external use"""
    return vault_sync.sync_vaults() 