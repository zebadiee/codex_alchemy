from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db import get_session
from backend.models import Glyph, SigilMetadata
from typing import List, Optional

router = APIRouter(prefix="/api/vault", tags=["Vault"])

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