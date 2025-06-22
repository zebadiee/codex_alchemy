from fastapi import APIRouter, HTTPException
from codex_alchemy.rituals.refine_script import refine_script

router = APIRouter()

@router.post("/api/rituals/refine")
def refine_script_route(script_input: str):
    try:
        refined_output = refine_script(script_input)
        return {"refined": refined_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

