# cli.py

import click
from utils import catch_alchemy_errors, AlchemyError
from vault import bundle, ingest, _load_state
from glyphs import quote_all
from rituals import list_rituals, ritual
from share import share_backend
from assistant import assistant

@click.group()
def cli():
    """Codex Alchemy CLI"""
    pass

# ---------- Vault Commands ----------
@cli.group()
def vault():
    """Vault commands"""
    pass

@vault.command("bundle")
@click.argument("sigil")
def bundle_vault(sigil):
    click.echo(f"🔒 Bundling vault '{sigil}'...")
    bundle(sigil)

@vault.command("ingest")
@click.argument("file", type=click.Path(exists=True))
def ingest_vault(file):
    click.echo(f"📥 Ingesting vault from {file}...")
    ingest(file)

@vault.command("list")
def list_vaults():
    state = _load_state()
    vaults = state.get("vaults", {})
    if not vaults:
        click.secho("📭 No vaults found.", fg="yellow")
    else:
        click.secho("🏴 Vaults Available:", fg="cyan")
        for sigil, v in vaults.items():
            glyph_count = len(v.get("glyphs", []))
            ritual_count = len(v.get("rituals", []))
            click.echo(f"• {sigil}: {glyph_count} glyphs, {ritual_count} rituals")

# ---------- Glyph Commands ----------
@cli.group()
def glyph():
    """Glyph commands"""
    pass

@glyph.command("quote")
@click.argument("scope", default="all")
@click.option("--format", default="table")
def quote_glyphs(scope, format):
    quote_all(scope=scope, format=format)

# ---------- Ritual Commands ----------
@cli.group()
def ritual():
    """Ritual commands"""
    pass

@ritual.command("list")
def list_rituals_command():
    list_rituals()

@ritual.command("run")
def run_ritual():
    ritual()

# ---------- Share Commands ----------
@cli.group()
def share():
    """Share Codex services"""
    pass

@share.command("backend")
def expose_backend():
    share_backend()

# ---------- Assistant Commands ----------
cli.add_command(assistant, name="assist")

from assistant import assistant
cli.add_command(assistant, name="assist")

