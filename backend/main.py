from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import gene_invoke
from .db import Base, engine
from .models import Ritual

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gene_invoke.router)

Base.metadata.create_all(bind=engine)

