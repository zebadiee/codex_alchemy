"""
Gene Assistant API Routes
Provides symbolic assistance with ritual awareness and offline capabilities
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
from datetime import datetime

router = APIRouter()

class GeneRequest(BaseModel):
    prompt: str
    context: Dict[str, Any]

class GeneResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = None
    ritual_hint: Optional[str] = None
    offline: bool = False

class GeneAssistant:
    def __init__(self):
        self.ledger_path = ".vault/ledger/assistant_log.jsonl"
        self.ensure_ledger_directory()
    
    def ensure_ledger_directory(self):
        """Ensure the ledger directory exists"""
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
    
    def log_interaction(self, prompt: str, response: str, context: Dict[str, Any]):
        """Log interaction to the ledger"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "context": context
        }
        
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_ritual_knowledge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get ritual-specific knowledge based on context"""
        knowledge = {
            "dream_loop": {
                "description": "Evolves glyphs through symbolic mutation",
                "command": "python unified_cli.py dream-loop",
                "output": "Creates evolved glyphs with 🧬 suffix",
                "related": ["vault diff", "sync-status", "evolve"]
            },
            "vault_diff": {
                "description": "Compare two sigils in the vault",
                "command": "codex-alchemy vault diff <sigil_a> <sigil_b>",
                "output": "Shows differences between sigils",
                "related": ["vault list", "vault reflect", "dream-loop"]
            },
            "vault_sync": {
                "description": "Synchronize vaults between Codex and A0",
                "command": "python unified_cli.py sync",
                "output": "Bi-directional vault synchronization",
                "related": ["sync-status", "vault diff", "a0-integration"]
            },
            "glyphs": {
                "description": "Symbolic entities stored in vaults",
                "command": "codex-alchemy vault list",
                "output": "List all available sigils",
                "related": ["vault restore", "vault reflect", "dream-loop"]
            }
        }
        return knowledge
    
    def analyze_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context to provide relevant assistance"""
        analysis = {
            "current_page": context.get("page", "unknown"),
            "recent_ritual": context.get("recentRitual"),
            "active_vault": context.get("vault", "default"),
            "glyph_count": context.get("glyphs", 0),
            "last_sync": context.get("lastSync"),
            "suggestions": []
        }
        
        # Page-specific suggestions
        if "rituals" in context.get("page", ""):
            analysis["suggestions"].extend(["dream-loop", "vault diff", "sync-status"])
        elif "glyphs" in context.get("page", ""):
            analysis["suggestions"].extend(["vault list", "vault reflect", "dream-loop"])
        elif "a0" in context.get("page", ""):
            analysis["suggestions"].extend(["sync", "a0-status", "vault diff"])
        
        # Recent ritual suggestions
        if context.get("recentRitual"):
            analysis["suggestions"].extend(["vault diff", "sync-status", "glyphs"])
        
        return analysis
    
    def generate_response(self, prompt: str, context: Dict[str, Any]) -> GeneResponse:
        """Generate a contextual response"""
        prompt_lower = prompt.lower()
        analysis = self.analyze_context(context)
        knowledge = self.get_ritual_knowledge(context)
        
        # Determine response type
        if any(word in prompt_lower for word in ["dream", "loop", "evolve", "mutation"]):
            ritual_info = knowledge["dream_loop"]
            response = f"I can help with the dream loop ritual! {ritual_info['description']}. Try `{ritual_info['command']}` to evolve your glyphs."
            suggestions = ritual_info["related"]
            ritual_hint = f"The dream loop creates evolved glyphs with 🧬 mutations from your current sigil."
            
        elif any(word in prompt_lower for word in ["vault", "diff", "compare", "sigil"]):
            ritual_info = knowledge["vault_diff"]
            response = f"Vault comparison is powerful! {ritual_info['description']}. Use `{ritual_info['command']}` to see differences."
            suggestions = ritual_info["related"]
            ritual_hint = "Vault diff shows exactly what changed between sigils."
            
        elif any(word in prompt_lower for word in ["sync", "synchronize", "a0"]):
            ritual_info = knowledge["vault_sync"]
            response = f"Vault synchronization connects Codex and A0! {ritual_info['description']}. Run `{ritual_info['command']}` to sync."
            suggestions = ritual_info["related"]
            ritual_hint = "Sync preserves differences while merging common elements."
            
        elif any(word in prompt_lower for word in ["glyph", "symbol", "entity"]):
            ritual_info = knowledge["glyphs"]
            response = f"Glyphs are symbolic entities in your vault! {ritual_info['description']}. Use `{ritual_info['command']}` to explore."
            suggestions = ritual_info["related"]
            ritual_hint = f"Your vault currently contains {analysis['glyph_count']} glyphs."
            
        elif any(word in prompt_lower for word in ["help", "assist", "guide"]):
            response = "I am Gene, your symbolic assistant! I can help with rituals, vaults, glyphs, and the dream loop evolution. What would you like to explore?"
            suggestions = ["dream-loop", "vault diff", "sync", "glyphs"]
            ritual_hint = "Press Ctrl+Shift+G anytime to summon me for assistance."
            
        else:
            # Default response with context awareness
            response = f"I sense you're working with {analysis['current_page']}. How can I assist with your symbolic journey?"
            suggestions = analysis["suggestions"] or ["dream-loop", "vault diff", "sync"]
            ritual_hint = "I'm aware of your current context and can provide targeted assistance."
        
        return GeneResponse(
            response=response,
            suggestions=suggestions,
            ritual_hint=ritual_hint
        )

# Initialize Gene Assistant
gene = GeneAssistant()

@router.post("/respond", response_model=GeneResponse)
async def respond_to_gene(request: GeneRequest):
    """Respond to Gene Assistant requests with ritual awareness"""
    try:
        # Generate response
        response = gene.generate_response(request.prompt, request.context)
        
        # Log interaction
        gene.log_interaction(request.prompt, response.response, request.context)
        
        return response
        
    except Exception as e:
        # Fallback to offline mode
        return GeneResponse(
            response="I'm experiencing some difficulties right now. Try asking about rituals, vaults, or glyphs.",
            suggestions=["dream-loop", "vault diff", "sync"],
            ritual_hint="I can still help with basic symbolic operations.",
            offline=True
        )

@router.get("/status")
async def gene_status():
    """Get Gene Assistant status and recent interactions"""
    try:
        if os.path.exists(gene.ledger_path):
            with open(gene.ledger_path, "r") as f:
                lines = f.readlines()
                recent_interactions = len(lines)
                last_interaction = json.loads(lines[-1]) if lines else None
        else:
            recent_interactions = 0
            last_interaction = None
        
        return {
            "status": "active",
            "recent_interactions": recent_interactions,
            "last_interaction": last_interaction,
            "ledger_path": gene.ledger_path
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        } 