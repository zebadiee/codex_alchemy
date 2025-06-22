from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from backend.drift_monitor import detect_drift

router = APIRouter()

@router.get("/drift/status")
def drift_status(sigil: str = Query("default")):
    result = detect_drift(sigil)
    return JSONResponse(result) 