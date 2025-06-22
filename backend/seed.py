import asyncio
from backend.db import async_engine, async_session_maker
from backend.models import Base, Ritual, Glyph
from sqlalchemy import text

rituals_to_seed = [
    {"name": "Script Synthesizer", "description": "Synthesizes code from text patterns"},
    {"name": "Deep Research", "description": "Launches AI-based research on specified themes"},
    {"name": "Agent Builder", "description": "Constructs task-specific AI agents"},
    {"name": "REPL Loop", "description": "Interactive correction loop with LLM"},
]

async def seed():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        # Clear existing data
        await session.execute(text("DELETE FROM glyphs"))
        await session.execute(text("DELETE FROM rituals"))
        await session.commit()

        # Add rituals
        ritual1 = Ritual(name="Morning Ritual", description="Start your day with intention.")
        ritual2 = Ritual(name="Evening Ritual", description="Reflect and unwind.")
        session.add_all([ritual1, ritual2])
        await session.flush()

        # Add glyphs
        glyphs = [
            Glyph(symbol="☀️", ritual_id=ritual1.id),
            Glyph(symbol="🌙", ritual_id=ritual2.id),
            Glyph(symbol="🔥", ritual_id=ritual1.id),
        ]
        session.add_all(glyphs)
        await session.commit()
    print("🌱 Rituals seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed()) 