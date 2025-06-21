# backend/routes/rituals.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/rituals")
def get_rituals():
    return [{"id": 1, "name": "Morning Ritual", "description": "Start your day with intention."}]

# --- Dream Loop Endpoint ---
from codex_alchemy.rituals.evolve import evolve_glyphs
from codex_alchemy.vault import restore, preserve

@router.post("/dream-loop")
def dream_loop():
    # Use 'default' as the source sigil and 'evolved' as the target
    source_sigil = "default"
    target_sigil = "evolved"
    glyphs = restore(source_sigil)
    if not glyphs:
        # Create seed glyphs if none exist
        import numpy as np
        from codex_alchemy.vault import Glyph
        seed_glyphs = []
        for i in range(3):
            vector = np.random.normal(0, 1, 10).tolist()
            glyph = Glyph(name=f"seed_glyph_{i}", vector=vector)
            seed_glyphs.append(glyph)
        preserve(source_sigil, seed_glyphs)
        glyphs = seed_glyphs
    evolve_glyphs(source_sigil, target_sigil)
    evolved_glyphs = restore(target_sigil)
    return JSONResponse({
        "status": "success",
        "evolved_glyphs": len(evolved_glyphs),
        "iterations": 1,
        "lineage_depth": 1,
        "new_glyphs": [{"name": g.name} for g in evolved_glyphs]
    })

