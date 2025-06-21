# codex_alchemy/cli.py

import click
from codex_alchemy.vault import list_sigils, reflect_all, restore, preserve
from codex_alchemy.rituals.evolve import evolve_glyphs
from codex_alchemy.debugger import debug  # 🔧 This is the debug command function

@click.group()
def cli():
    """Codex Alchemy CLI"""
    pass

# 🔁 Attach debug command AFTER cli() is defined
cli.add_command(debug, name="debug")

@cli.group()
def vault():
    """Vault sigil operations"""
    pass

@vault.command()
def list():
    """List all sigils"""
    list_sigils()

@vault.command()
@click.argument('reflection_sigil')
def reflect(reflection_sigil):
    """Reflect vault into new sigil"""
    reflect_all(reflection_sigil)

@vault.command()
@click.argument('sigil')
def restore_cmd(sigil):
    """Restore sigil glyphs"""
    restore(sigil)

@vault.command()
@click.argument('sigil')
@click.argument('output_path')
def preserve_cmd(sigil, output_path):
    """Preserve sigil to path"""
    glyphs = restore(sigil)
    preserve(output_path, glyphs)

@vault.command("evolve")
@click.argument("input_sigil")
@click.argument("output_sigil")
def evolve_cmd(input_sigil, output_sigil):
    """Evolve glyphs from one sigil to another."""
    evolve_glyphs(input_sigil, output_sigil)

