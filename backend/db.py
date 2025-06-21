from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./spiral_codex.db"

async_engine = create_async_engine(
    DATABASE_URL, echo=True
)
async_session_maker = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()

# Dependency for FastAPI
async def get_session():
    async with async_session_maker() as session:
        yield session 