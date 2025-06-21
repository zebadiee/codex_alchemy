from fastapi import APIRouter, Body
from rituals.refine_script import refine_script

router = APIRouter()

@router.post("/refine-script")
def refine(script: str = Body(...), feedback: dict = Body(...)):
    refined = refine_script(script, feedback)
    return {"refined_script": refined} 