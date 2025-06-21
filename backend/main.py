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
    allow_origins=origins,
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

@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

