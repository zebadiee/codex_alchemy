# codex_alchemy/rituals/evolve.py
import click
from codex_alchemy.vault import restore, preserve, Glyph
from codex_alchemy.utils import log
import numpy as np


def mutate_vector(vector):
    noise = np.random.normal(0, 0.05, size=len(vector))
    return (np.array(vector) + noise).tolist()


@click.command()
@click.argument("source_sigil")
@click.argument("target_sigil")
def evolve_cli(source_sigil, target_sigil):
    log(f"🌱 Evolving glyphs from '{source_sigil}' → '{target_sigil}'")
    glyphs = restore(source_sigil)

    evolved = []
    for glyph in glyphs:
        new_vec = mutate_vector(glyph.vector)
        new_name = f"{glyph.name}_evolved"
        evolved_glyph = Glyph(name=new_name, vector=new_vec)
        evolved.append(evolved_glyph)
        log(f"🧬 Evolved {glyph.name} → {new_name}")

    preserve(target_sigil, evolved)
    log(f"✅ Evolution complete. {len(evolved)} glyphs saved under '{target_sigil}'")

