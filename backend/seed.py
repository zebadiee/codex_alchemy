import asyncio
from backend.db import async_engine, async_session_maker
from backend.models import Base, Ritual

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
        for ritual in rituals_to_seed:
            session.add(Ritual(**ritual))
        await session.commit()
    print("🌱 Rituals seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed()) 