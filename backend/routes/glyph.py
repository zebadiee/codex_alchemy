from fastapi import APIRouter, Query, Response, Body
from codex_alchemy.utils.shape_grammar import evolve_glyph
from codex_alchemy.utils.svg_export import glyph_to_svg

router = APIRouter()

@router.get("/api/glyph/generate")
def generate_glyph(
    steps: int = Query(5, description="Evolution steps"),
    grammar: str = Query("default", description="Grammar style"),
    format: str = Query("json", description="Output format: json or svg")
):
    chain = evolve_glyph(steps=steps, grammar=grammar)
    glyph = chain[-1]
    if format == "svg":
        svg = glyph_to_svg(glyph)
        return Response(content=svg, media_type="image/svg+xml")
    return glyph

@router.post("/api/glyph/evolve")
def evolve_ritual(
    steps: int = Body(5),
    grammar: str = Body("default"),
    format: str = Body("svg")
):
    chain = evolve_glyph(steps=steps, grammar=grammar)
    glyph = chain[-1]
    if format == "svg":
        svg = glyph_to_svg(glyph)
        return Response(content=svg, media_type="image/svg+xml")
    return glyph

@router.post("/api/glyph/mutate")
def mutate_ritual(
    glyph: dict = Body(...),
    format: str = Body("svg")
):
    # For now, mutate = evolve one step from current glyph
    from codex_alchemy.utils.shape_grammar import apply_phased_rules
    mutated = apply_phased_rules(glyph, grammar="default")
    if isinstance(mutated, list):
        mutated = mutated[0]
    if format == "svg":
        svg = glyph_to_svg(mutated)
        return Response(content=svg, media_type="image/svg+xml")
    return mutated

@router.post("/api/glyph/compress")
def compress_ritual(
    glyph: dict = Body(...),
    format: str = Body("json")
):
    from codex_alchemy.utils.compression import compress_glyphs
    compressed = compress_glyphs([glyph])
    if format == "json":
        return {"compressed": compressed}
    return compressed 