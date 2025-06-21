# codex_alchemy/debugger.py

import click
from codex_alchemy.rituals.evolve import evolve_glyphs
from codex_alchemy.vault import restore
from codex_alchemy.utils import log

@click.command(name="debug")
@click.option("--ritual", required=True, type=click.Choice(["evolve"], case_sensitive=False))
@click.option("--input", "input_sigil", required=True)
@click.option("--output", "output_sigil", required=True)
def debug_cmd(ritual, input_sigil, output_sigil):
    """Run debug routines on rituals."""
    log(f"🧪 Debugging ritual: {ritual}")
    if ritual == "evolve":
        glyphs = restore(input_sigil)
        log(f"🔍 Found {len(glyphs)} glyphs in 🪬 '{input_sigil}'")
        for g in glyphs:
            log(f"🔹 {g.name} ({len(g.vector)} dims)")
        evolve_glyphs(input_sigil, output_sigil)
        log(f"🧠 Ritual '{ritual}' complete")

# 👇 THIS IS CRITICAL
__all__ = ["debug_cmd"]

