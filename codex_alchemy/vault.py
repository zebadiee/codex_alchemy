import os
import json
from codex_alchemy.utils import log, catch_alchemy_errors
from dataclasses import dataclass, asdict

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".vault", "sigils"))
os.makedirs(VAULT_DIR, exist_ok=True)

@dataclass
class Glyph:
    name: str
    vector: list

@catch_alchemy_errors
def restore(sigil: str):
    path = os.path.join(VAULT_DIR, f"{sigil}.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Vault sigil '{sigil}' not found at {path}")

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Vault file '{sigil}.json' is not valid JSON: {e}")

    if not isinstance(data, list):
        raise ValueError(f"Vault file for sigil '{sigil}' must be a list of glyphs.")

    glyphs = []
    for entry in data:
        if not isinstance(entry, dict) or "name" not in entry or "vector" not in entry:
            raise ValueError(f"Malformed glyph entry in sigil '{sigil}': {entry}")
        glyphs.append(Glyph(name=entry["name"], vector=entry["vector"]))

    if not glyphs:
        raise ValueError(f"Sigil '{sigil}' contains zero glyphs.")

    log(f"📦 Restored {len(glyphs)} glyphs from '{sigil}'")
    for g in glyphs[:20]:
        log(f"🔹 {g.name} ({len(g.vector)} dims)")
    return glyphs


@catch_alchemy_errors
def preserve(sigil: str, glyphs: list):
    path = os.path.join(VAULT_DIR, f"{sigil}.json")
    with open(path, "w") as f:
        json.dump([asdict(g) for g in glyphs], f, indent=2)
    log(f"💾 Vault saved successfully to '{sigil}'")


@catch_alchemy_errors
def list_sigils():
    sigils = [f[:-5] for f in os.listdir(VAULT_DIR) if f.endswith(".json")]
    log("🔍 Available sigils:")
    for s in sigils:
        log(f"  • {s}")
    return sigils


@catch_alchemy_errors
def reflect_all(reflection_sigil: str):
    all_glyphs = []
    for sigil in list_sigils():
        if sigil == reflection_sigil:
            continue
        glyphs = restore(sigil)
        if glyphs:
            all_glyphs.extend(glyphs)
    preserve(reflection_sigil, all_glyphs)
    log(f"🪞 Reflected all glyphs into '{reflection_sigil}'")


@catch_alchemy_errors
def ingest(sigil: str, glyphs: list):
    existing = restore(sigil) or []
    preserve(sigil, existing + glyphs)
    log(f"➕ Ingested {len(glyphs)} glyphs into '{sigil}'")


@catch_alchemy_errors
def bundle(sigils: list, bundle_name: str):
    bundled = []
    for sigil in sigils:
        glyphs = restore(sigil)
        if glyphs:
            bundled.extend(glyphs)
    preserve(bundle_name, bundled)
    log(f"📦 Bundled {len(sigils)} sigils into '{bundle_name}'")
@catch_alchemy_errors
def preserve(sigil: str, glyphs: list):
    path = os.path.join(VAULT_DIR, f"{sigil}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [{"name": glyph.name, "vector": glyph.vector} for glyph in glyphs]

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    log(f"📝 Preserved {len(glyphs)} glyphs under sigil '{sigil}' → {path}")

