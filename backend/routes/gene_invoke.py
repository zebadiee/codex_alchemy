from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Ritual

router = APIRouter(prefix="/api/gene", tags=["Gene Assistant"])

# Simple input model
class GenePrompt(BaseModel):
    prompt: str

# Placeholder Gene logic
@router.post("/invoke")
async def invoke_gene(prompt: GenePrompt, request: Request):
    user_ip = request.client.host
    return {
        "from": "Gene",
        "ip": user_ip,
        "input": prompt.prompt,
        "output": f"🧠 Gene is reflecting on: '{prompt.prompt}'..."
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rituals")
def read_rituals(db: Session = Depends(get_db)):
    return db.query(Ritual).all()
