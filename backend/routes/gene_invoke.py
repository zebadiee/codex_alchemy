from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.db import get_session
from backend.models import Ritual, Glyph, SigilMetadata
from typing import List, Optional

router = APIRouter(prefix="/api/gene", tags=["Gene Assistant"])

# Pydantic models
class GenePrompt(BaseModel):
    prompt: str

class RitualCreate(BaseModel):
    name: str
    description: str

class GlyphResponse(BaseModel):
    id: int
    name: str
    hash: str
    vector: List[float]
    symbol: Optional[str]
    glyph_type: str
    ritual_id: Optional[int]
    created_at: str

class RitualResponse(BaseModel):
    id: int
    name: str
    description: str
    ritual_type: str
    created_at: str
    glyphs: List[GlyphResponse]

@router.post("/invoke")
async def invoke_gene(prompt: GenePrompt):
    """Invoke the Gene assistant with a prompt"""
    return {"output": f"Gene processed: {prompt.prompt}"}

@router.post("/rituals")
async def create_ritual(ritual: RitualCreate, session: AsyncSession = Depends(get_session)):
    """Create a new ritual"""
    db_ritual = Ritual(name=ritual.name, description=ritual.description)
    session.add(db_ritual)
    await session.commit()
    await session.refresh(db_ritual)
    return {"id": db_ritual.id, "name": db_ritual.name, "description": db_ritual.description}

@router.get("/rituals")
async def read_rituals(session: AsyncSession = Depends(get_session)):
    """Get all rituals"""
    result = await session.execute(select(Ritual))
    rituals = result.scalars().all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "ritual_type": r.ritual_type,
            "created_at": r.created_at.isoformat(),
            "glyphs": []
        }
        for r in rituals
    ]

@router.get("/rituals_with_glyphs")
async def read_rituals_with_glyphs(session: AsyncSession = Depends(get_session)):
    """Get all rituals with their associated glyphs"""
    result = await session.execute(
        select(Ritual).options(selectinload(Ritual.glyphs))
    )
    rituals = result.scalars().all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "ritual_type": r.ritual_type,
            "created_at": r.created_at.isoformat(),
            "glyphs": [
                {
                    "id": g.id,
                    "name": g.name,
                    "hash": g.hash,
                    "vector": g.vector,
                    "symbol": g.symbol,
                    "glyph_type": g.glyph_type,
                    "created_at": g.created_at.isoformat()
                } for g in r.glyphs
            ]
        }
        for r in rituals
    ]

@router.get("/glyphs")
async def read_glyphs(
    glyph_type: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all glyphs, optionally filtered by type"""
    query = select(Glyph)
    if glyph_type:
        query = query.where(Glyph.glyph_type == glyph_type)
    
    result = await session.execute(query)
    glyphs = result.scalars().all()
    
    return [
        {
            "id": g.id,
            "name": g.name,
            "hash": g.hash,
            "vector": g.vector,
            "symbol": g.symbol,
            "glyph_type": g.glyph_type,
            "ritual_id": g.ritual_id,
            "created_at": g.created_at.isoformat()
        }
        for g in glyphs
    ]

@router.get("/glyphs/{glyph_id}")
async def read_glyph(glyph_id: int, session: AsyncSession = Depends(get_session)):
    """Get a specific glyph by ID"""
    result = await session.execute(select(Glyph).where(Glyph.id == glyph_id))
    glyph = result.scalar_one_or_none()
    
    if not glyph:
        raise HTTPException(status_code=404, detail="Glyph not found")
    
    return {
        "id": glyph.id,
        "name": glyph.name,
        "hash": glyph.hash,
        "vector": glyph.vector,
        "symbol": glyph.symbol,
        "glyph_type": glyph.glyph_type,
        "ritual_id": glyph.ritual_id,
        "created_at": glyph.created_at.isoformat()
    }

@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session)):
    """Get database statistics"""
    # Count glyphs by type
    result = await session.execute(select(Glyph.glyph_type))
    glyph_types = result.scalars().all()
    glyph_type_counts = {}
    for gt in glyph_types:
        glyph_type_counts[gt] = glyph_type_counts.get(gt, 0) + 1
    
    # Count rituals
    result = await session.execute(select(Ritual))
    ritual_count = len(result.scalars().all())
    
    # Get sigil metadata
    result = await session.execute(select(SigilMetadata))
    sigil_meta = result.scalars().first()
    
    return {
        "glyph_type_counts": glyph_type_counts,
        "total_rituals": ritual_count,
        "sigil_metadata": {
            "name": sigil_meta.sigil_name if sigil_meta else None,
            "description": sigil_meta.description if sigil_meta else None,
            "glyph_count": sigil_meta.glyph_count if sigil_meta else 0,
            "ritual_count": sigil_meta.ritual_count if sigil_meta else 0,
            "last_updated": sigil_meta.last_updated.isoformat() if sigil_meta else None
        }
    }
