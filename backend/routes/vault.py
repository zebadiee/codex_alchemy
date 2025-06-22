from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db import get_session
from backend.models import Glyph, SigilMetadata
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/vault", tags=["Vault"])

class SigilTreeRequest(BaseModel):
    sigil_name: str
    depth: Optional[int] = 3

class SigilTreeResponse(BaseModel):
    sigil_name: str
    glyphs: List[Dict[str, Any]]
    lineage: List[Dict[str, Any]]
    mutations: List[Dict[str, Any]]
    timestamp: str

@router.get("/glyphs")
async def get_vault_glyphs(
    glyph_type: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all evolved glyphs from the vault (database)"""
    query = select(Glyph)
    if glyph_type:
        query = query.where(Glyph.glyph_type == glyph_type)
    
    result = await session.execute(query)
    glyphs = result.scalars().all()
    
    return [
        {
            "name": g.name,
            "vector": g.vector,
            "hash": g.hash
        }
        for g in glyphs
    ]

@router.get("/glyphs/evolved")
async def get_evolved_glyphs(session: AsyncSession = Depends(get_session)):
    """Get only evolved glyphs (not ritual-generated)"""
    result = await session.execute(
        select(Glyph).where(Glyph.glyph_type == "evolved")
    )
    glyphs = result.scalars().all()
    
    return [
        {
            "name": g.name,
            "vector": g.vector,
            "hash": g.hash
        }
        for g in glyphs
    ]

@router.get("/glyphs/ritual-generated")
async def get_ritual_glyphs(session: AsyncSession = Depends(get_session)):
    """Get only ritual-generated glyphs"""
    result = await session.execute(
        select(Glyph).where(Glyph.glyph_type == "ritual_generated")
    )
    glyphs = result.scalars().all()
    
    return [
        {
            "name": g.name,
            "vector": g.vector,
            "hash": g.hash
        }
        for g in glyphs
    ]

@router.get("/metadata")
async def get_vault_metadata(session: AsyncSession = Depends(get_session)):
    """Get vault metadata and statistics"""
    result = await session.execute(select(SigilMetadata))
    sigil_meta = result.scalar_one_or_none()
    
    if not sigil_meta:
        raise HTTPException(status_code=404, detail="No vault metadata found")
    
    return {
        "sigil_name": sigil_meta.sigil_name,
        "description": sigil_meta.description,
        "glyph_count": sigil_meta.glyph_count,
        "ritual_count": sigil_meta.ritual_count,
        "last_updated": sigil_meta.last_updated.isoformat(),
        "meta_data": sigil_meta.meta_data
    }

@router.get("/stats")
async def get_vault_stats(session: AsyncSession = Depends(get_session)):
    """Get detailed vault statistics"""
    # Count glyphs by type
    result = await session.execute(select(Glyph.glyph_type))
    glyph_types = result.scalars().all()
    glyph_type_counts = {}
    for gt in glyph_types:
        glyph_type_counts[gt] = glyph_type_counts.get(gt, 0) + 1
    
    # Get total count
    result = await session.execute(select(Glyph))
    total_glyphs = len(result.scalars().all())
    
    # Get sigil metadata
    result = await session.execute(select(SigilMetadata))
    sigil_meta = result.scalar_one_or_none()
    
    return {
        "total_glyphs": total_glyphs,
        "glyph_type_counts": glyph_type_counts,
        "sigil_metadata": {
            "name": sigil_meta.sigil_name if sigil_meta else None,
            "description": sigil_meta.description if sigil_meta else None,
            "glyph_count": sigil_meta.glyph_count if sigil_meta else 0,
            "ritual_count": sigil_meta.ritual_count if sigil_meta else 0,
            "last_updated": sigil_meta.last_updated.isoformat() if sigil_meta else None
        }
    }

@router.get("/vault/sigils")
def get_sigils():
    """Get all available sigils"""
    try:
        sigil_dir = ".vault/sigils"
        if not os.path.exists(sigil_dir):
            return {"sigils": []}
        
        sigils = []
        for filename in os.listdir(sigil_dir):
            if filename.endswith('.json'):
                sigil_name = filename[:-5]  # Remove .json extension
                sigils.append({
                    "name": sigil_name,
                    "path": f"{sigil_dir}/{filename}",
                    "modified": datetime.fromtimestamp(
                        os.path.getmtime(f"{sigil_dir}/{filename}")
                    ).isoformat()
                })
        
        return {"sigils": sigils}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading sigils: {str(e)}")

@router.post("/vault/tree")
def get_sigil_tree(request: SigilTreeRequest):
    """Get lineage tree for a specific sigil"""
    try:
        sigil_path = f".vault/sigils/{request.sigil_name}.json"
        
        if not os.path.exists(sigil_path):
            raise HTTPException(status_code=404, detail=f"Sigil '{request.sigil_name}' not found")
        
        # Read the sigil data
        with open(sigil_path, 'r') as f:
            glyphs_data = json.load(f)
        
        # Analyze glyph lineage and mutations
        lineage = []
        mutations = []
        
        for glyph in glyphs_data:
            glyph_info = {
                "name": glyph.get("name", "unknown"),
                "hash": glyph.get("hash", ""),
                "vector_length": len(glyph.get("vector", [])),
                "created": glyph.get("created", datetime.now().isoformat()),
                "parent": glyph.get("parent", None),
                "mutation_type": glyph.get("mutation_type", "seed")
            }
            
            lineage.append(glyph_info)
            
            # Track mutations
            if glyph.get("mutation_type") != "seed":
                mutations.append({
                    "glyph_name": glyph["name"],
                    "mutation_type": glyph.get("mutation_type", "unknown"),
                    "parent": glyph.get("parent", "unknown"),
                    "timestamp": glyph.get("created", datetime.now().isoformat())
                })
        
        # Get related sigils (sigils that might be parents or children)
        related_sigils = []
        sigil_dir = ".vault/sigils"
        if os.path.exists(sigil_dir):
            for filename in os.listdir(sigil_dir):
                if filename.endswith('.json') and filename != f"{request.sigil_name}.json":
                    related_sigil_name = filename[:-5]
                    related_sigils.append(related_sigil_name)
        
        return SigilTreeResponse(
            sigil_name=request.sigil_name,
            glyphs=glyphs_data,
            lineage=lineage,
            mutations=mutations,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sigil tree: {str(e)}")

@router.get("/vault/lineage/{sigil_name}")
def get_sigil_lineage(sigil_name: str):
    """Get detailed lineage information for a sigil"""
    try:
        sigil_path = f".vault/sigils/{sigil_name}.json"
        
        if not os.path.exists(sigil_path):
            raise HTTPException(status_code=404, detail=f"Sigil '{sigil_name}' not found")
        
        with open(sigil_path, 'r') as f:
            glyphs_data = json.load(f)
        
        # Build lineage graph
        lineage_graph = {
            "nodes": [],
            "edges": [],
            "metadata": {
                "sigil_name": sigil_name,
                "total_glyphs": len(glyphs_data),
                "seed_glyphs": len([g for g in glyphs_data if g.get("mutation_type") == "seed"]),
                "mutated_glyphs": len([g for g in glyphs_data if g.get("mutation_type") != "seed"])
            }
        }
        
        # Add nodes
        for glyph in glyphs_data:
            node = {
                "id": glyph["name"],
                "name": glyph["name"],
                "type": glyph.get("mutation_type", "seed"),
                "hash": glyph.get("hash", ""),
                "vector_length": len(glyph.get("vector", [])),
                "created": glyph.get("created", datetime.now().isoformat())
            }
            lineage_graph["nodes"].append(node)
            
            # Add edges for parent relationships
            if glyph.get("parent"):
                edge = {
                    "source": glyph["parent"],
                    "target": glyph["name"],
                    "type": "mutation",
                    "mutation_type": glyph.get("mutation_type", "unknown")
                }
                lineage_graph["edges"].append(edge)
        
        return lineage_graph
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating lineage: {str(e)}")

@router.get("/vault/tree")
def get_sigil_tree(sigil: str = Query(...)):
    """Return the lineage tree for a sigil"""
    import os, json
    sigil_dir = ".vault/sigils"
    sigil_path = os.path.join(sigil_dir, f"{sigil}.json")
    if not os.path.exists(sigil_path):
        return JSONResponse(status_code=404, content={"error": f"Sigil '{sigil}' not found"})
    
    with open(sigil_path) as f:
        sigil_data = json.load(f)
    
    # Handle both array format and object with glyphs field
    if isinstance(sigil_data, list):
        glyphs = sigil_data
    else:
        glyphs = sigil_data.get("glyphs", [])
    
    # Build tree structure for react-d3-tree
    tree_nodes = []
    node_map = {}
    
    # Create nodes for each glyph
    for glyph in glyphs:
        glyph_name = glyph.get("name", "unknown")
        node = {
            "name": glyph_name,
            "attributes": {
                "hash": glyph.get("hash", ""),
                "vector_length": len(glyph.get("vector", [])),
                "mutation_type": glyph.get("mutation_type", "seed"),
                "timestamp": glyph.get("created", datetime.now().isoformat())
            },
            "children": []
        }
        tree_nodes.append(node)
        node_map[glyph_name] = node
    
    # Build parent-child relationships
    root_nodes = []
    for glyph in glyphs:
        glyph_name = glyph.get("name", "unknown")
        parent_name = glyph.get("parent")
        
        if parent_name and parent_name in node_map:
            # Add as child to parent
            node_map[parent_name]["children"].append(node_map[glyph_name])
        else:
            # This is a root node
            root_nodes.append(node_map[glyph_name])
    
    # If no root nodes found, use all nodes as roots
    if not root_nodes:
        root_nodes = tree_nodes
    
    # Return the tree structure
    return {
        "name": sigil,
        "children": root_nodes,
        "metadata": {
            "total_glyphs": len(glyphs),
            "root_nodes": len(root_nodes),
            "timestamp": datetime.now().isoformat()
        }
    } 