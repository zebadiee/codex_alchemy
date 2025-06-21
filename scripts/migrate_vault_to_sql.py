#!/usr/bin/env python3
"""
Vault to SQL Migration Script
Migrates evolved glyph data from codex_vault_backup.json to SQLite database
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from backend.db import async_engine, async_session_maker
from backend.models import Base, Ritual, Glyph, SigilMetadata
from sqlalchemy import text

VAULT_BACKUP_PATH = Path(__file__).parent.parent / "codex_vault_backup.json"

async def create_tables():
    """Create all database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")

async def load_vault_data():
    """Load data from vault backup into database"""
    if not VAULT_BACKUP_PATH.exists():
        print(f"❌ Vault backup not found at {VAULT_BACKUP_PATH}")
        return
    
    print(f"📖 Loading vault data from {VAULT_BACKUP_PATH}")
    
    with open(VAULT_BACKUP_PATH, 'r') as f:
        vault_data = json.load(f)
    
    async with async_session_maker() as session:
        # Clear existing data
        await session.execute(text("DELETE FROM glyphs"))
        await session.execute(text("DELETE FROM rituals"))
        await session.execute(text("DELETE FROM sigil_metadata"))
        await session.commit()
        
        # Process RecoveredSigil data
        recovered_sigil = vault_data.get("RecoveredSigil", [])
        print(f"🔍 Found {len(recovered_sigil)} glyphs in RecoveredSigil")
        
        glyph_count = 0
        ritual_count = 0
        
        for item in recovered_sigil:
            name = item.get("name", "")
            vector = item.get("vector", [])
            hash_value = item.get("hash", "")
            
            if not name or not vector:
                continue
            
            # Determine if this is a ritual or glyph based on name
            if name.startswith("deduction_ritual_"):
                # Create ritual
                ritual = Ritual(
                    name=name,
                    description=f"Evolved deduction ritual {name}",
                    ritual_type="deduction",
                    created_at=datetime.utcnow()
                )
                session.add(ritual)
                await session.flush()
                
                # Create glyph for the ritual
                glyph = Glyph(
                    name=name,
                    hash=hash_value,
                    vector=vector,
                    ritual_id=ritual.id,
                    glyph_type="ritual_generated",
                    created_at=datetime.utcnow()
                )
                session.add(glyph)
                ritual_count += 1
            else:
                # Create standalone glyph
                glyph = Glyph(
                    name=name,
                    hash=hash_value,
                    vector=vector,
                    glyph_type="evolved",
                    created_at=datetime.utcnow()
                )
                session.add(glyph)
                glyph_count += 1
        
        # Create sigil metadata
        sigil_meta = SigilMetadata(
            sigil_name="RecoveredSigil",
            description="Evolved glyphs recovered from ritual evolution process",
            glyph_count=glyph_count,
            ritual_count=ritual_count,
            last_updated=datetime.utcnow(),
            meta_data={
                "source": "codex_vault_backup.json",
                "migration_date": datetime.utcnow().isoformat(),
                "total_items": len(recovered_sigil)
            }
        )
        session.add(sigil_meta)
        
        await session.commit()
        
        print(f"✅ Migration complete:")
        print(f"   • {glyph_count} standalone glyphs")
        print(f"   • {ritual_count} rituals with glyphs")
        print(f"   • Total items: {glyph_count + ritual_count}")

async def verify_migration():
    """Verify the migration was successful"""
    async with async_session_maker() as session:
        # Count glyphs
        result = await session.execute(text("SELECT COUNT(*) FROM glyphs"))
        glyph_count = result.scalar()
        
        # Count rituals
        result = await session.execute(text("SELECT COUNT(*) FROM rituals"))
        ritual_count = result.scalar()
        
        # Count sigil metadata
        result = await session.execute(text("SELECT COUNT(*) FROM sigil_metadata"))
        sigil_count = result.scalar()
        
        print(f"🔍 Verification:")
        print(f"   • Glyphs in DB: {glyph_count}")
        print(f"   • Rituals in DB: {ritual_count}")
        print(f"   • Sigil metadata: {sigil_count}")
        
        # Show sample data
        result = await session.execute(text("SELECT name, hash FROM glyphs LIMIT 5"))
        sample_glyphs = result.fetchall()
        print(f"   • Sample glyphs: {[g[0] for g in sample_glyphs]}")

async def main():
    """Main migration function"""
    print("🚀 Starting Vault to SQL Migration")
    print("=" * 50)
    
    try:
        await create_tables()
        await load_vault_data()
        await verify_migration()
        print("=" * 50)
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 