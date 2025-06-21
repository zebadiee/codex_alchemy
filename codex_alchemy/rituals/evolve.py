import time
import click
import numpy as np
from codex_alchemy.vault import restore, preserve, Glyph
from codex_alchemy.utils import log

def ritual_timer(func):
    def wrapper(*args, **kwargs):
        log("⏳ Initiating ritual evolution...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        log(f"⏱️ Ritual completed in {end - start:.2f}s")
        return result
    return wrapper

def mutate_vector(vector):
    noise = np.random.normal(0, 0.05, size=len(vector))
    return (np.array(vector) + noise).tolist()

@ritual_timer
def evolve_glyphs(source_sigil, target_sigil):
    log(f"🌱 Evolving glyphs from 🪬 '{source_sigil}' → 🧿 '{target_sigil}'")
    glyphs = restore(source_sigil)

    evolved = []
    for glyph in glyphs:
        new_vec = mutate_vector(glyph.vector)
        new_name = f"{glyph.name}_🧬"
        evolved_glyph = Glyph(name=new_name, vector=new_vec)
        evolved.append(evolved_glyph)
        log(f"🧠 {glyph.name} → {new_name}")

    preserve(target_sigil, evolved)
    log(f"✅ {len(evolved)} glyphs consecrated under 🔮 '{target_sigil}'")

