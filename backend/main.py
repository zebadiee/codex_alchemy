from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import gene_invoke
from backend.routes.vault import router as vault_router
from backend.db import Base, async_engine
from backend.models import Ritual
from fastapi import FastAPI
from backend.routes.rituals import router as rituals_router
from backend.routes.a0_integration import router as a0_router
from backend.routes.sync import router as sync_router
from backend.routes import refinement
from backend.routes.assistant import router as assistant_router
from backend.routes.drift import router as drift_router
from codex_alchemy.integrations.api_interceptor import TokenLimitInterceptor
from codex_alchemy.utils.compression import compress, decompress
from codex_alchemy.utils.token_optimizer import analyze_tokens
from backend.routes.glyph import router as glyph_router

app = FastAPI()

app.include_router(rituals_router, prefix="/api")


# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gene_invoke.router)
app.include_router(vault_router)
app.include_router(a0_router)
app.include_router(sync_router)
app.include_router(refinement.router, prefix="/api")
app.include_router(assistant_router, prefix="/api/assistant")
app.include_router(drift_router, prefix="/api")
app.include_router(glyph_router)

# Add TokenLimitInterceptor middleware
app.add_middleware(TokenLimitInterceptor)

@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/compression/stats")
def compression_stats(data: dict):
    """Return compression and token stats for given data."""
    compressed = compress(data)
    decompressed = decompress(compressed)
    stats = {
        "original_length": len(str(data)),
        "compressed_length": len(str(compressed)),
        "decompressed_length": len(str(decompressed)),
        "token_analysis": analyze_tokens(str(data)),
    }
    return stats

