from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db import get_session
from ..models import Ritual

router = APIRouter(prefix="/api/gene", tags=["Gene Assistant"])

# Simple input model
class GenePrompt(BaseModel):
    prompt: str

class RitualCreate(BaseModel):
    name: str
    description: str

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

@router.get("/rituals")
async def read_rituals(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ritual))
    rituals = result.scalars().all()
    return rituals

@router.post("/rituals", response_model=dict)
async def create_ritual(ritual: RitualCreate, session: AsyncSession = Depends(get_session)):
    new_ritual = Ritual(name=ritual.name, description=ritual.description)
    session.add(new_ritual)
    await session.commit()
    return {"status": "created", "ritual": ritual}
