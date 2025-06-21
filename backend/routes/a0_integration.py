"""
A0 Integration API Routes
Provides endpoints to access a0 functionality from codex_alchemy
"""

from fastapi import APIRouter, HTTPException
from backend.bridge_a0 import a0_bridge
from typing import List, Dict, Any

router = APIRouter(prefix="/api/a0", tags=["A0 Integration"])

@router.get("/status")
async def get_a0_status():
    """Get a0 system status"""
    return {
        "available": a0_bridge.is_a0_available(),
        "agents": a0_bridge.get_a0_agents(),
        "spells_count": len(a0_bridge.get_a0_spells()),
        "has_lineage": bool(a0_bridge.get_a0_lineage())
    }

@router.get("/agents")
async def get_a0_agents():
    """Get available a0 agents"""
    if not a0_bridge.is_a0_available():
        raise HTTPException(status_code=404, detail="A0 system not available")
    
    return {
        "agents": a0_bridge.get_a0_agents(),
        "total": len(a0_bridge.get_a0_agents())
    }

@router.get("/spells")
async def get_a0_spells():
    """Get spells from a0 vault"""
    if not a0_bridge.is_a0_available():
        raise HTTPException(status_code=404, detail="A0 system not available")
    
    spells = a0_bridge.get_a0_spells()
    return {
        "spells": spells,
        "total": len(spells)
    }

@router.get("/lineage")
async def get_a0_lineage():
    """Get lineage data from a0 vault"""
    if not a0_bridge.is_a0_available():
        raise HTTPException(status_code=404, detail="A0 system not available")
    
    return a0_bridge.get_a0_lineage()

@router.get("/vault/merged")
async def get_merged_vaults():
    """Get merged view of both codex_alchemy and a0 vaults"""
    return a0_bridge.merge_vaults()

@router.post("/agent/{agent_name}/invoke")
async def invoke_a0_agent(agent_name: str, payload: Dict[str, Any]):
    """Invoke an a0 agent"""
    if not a0_bridge.is_a0_available():
        raise HTTPException(status_code=404, detail="A0 system not available")
    
    agent = a0_bridge.import_a0_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        # This is a placeholder - actual implementation depends on a0 agent interface
        result = {
            "agent": agent_name,
            "status": "invoked",
            "payload": payload,
            "result": "Agent invoked successfully (placeholder)"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking agent: {str(e)}")

@router.get("/bridge/test")
async def test_a0_bridge():
    """Test a0 bridge functionality"""
    return {
        "bridge_available": a0_bridge.is_a0_available(),
        "a0_path": str(a0_bridge.a0_path),
        "a0_vault_path": str(a0_bridge.a0_vault_path),
        "codex_vault_path": str(a0_bridge.codex_vault_path),
        "agents": a0_bridge.get_a0_agents(),
        "spells": len(a0_bridge.get_a0_spells()),
        "lineage": bool(a0_bridge.get_a0_lineage())
    } 