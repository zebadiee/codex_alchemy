#!/bin/bash
set -e

echo "🧙 Generating complete Codex Alchemy system..."

# utils.py
cat > utils.py <<CODE
import click
class AlchemyError(Exception):
    pass

def catch_alchemy_errors(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AlchemyError as e:
            click.secho(f"🛑 Alchemy Error: {e}", fg="red")
        except Exception as e:
            click.secho(f"🔥 Unexpected Error: {e}", fg="yellow")
            raise
    return wrapper
CODE

# vault.py
cat > vault.py <<CODE
import json, os
from utils import catch_alchemy_errors

STATE_PATH = "spiral_cloud.vault.json"

def _load_state():
    if not os.path.exists(STATE_PATH):
        return {"vaults": {}}
    with open(STATE_PATH, "r") as f:
        return json.load(f)

def _save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

@catch_alchemy_errors
def bundle(sigil):
    print(f"🔒 Bundling vault '{sigil}' not implemented.")

@catch_alchemy_errors
def ingest(file):
    import click
    with open(file, "r") as f:
        vault_data = json.load(f)
    state = _load_state()
    if "vaults" not in state:
        state["vaults"] = {}
    sigil = vault_data.get("sigil", "default")
    state["vaults"][sigil] = vault_data
    _save_state(state)
    click.secho(f"✅ Vault '{sigil}' ingested.", fg="green")

def list_vaults():
    import click
    state = _load_state()
    if not state.get("vaults"):
        click.secho("📭 No vaults found.", fg="yellow")
        return
    click.secho("🏴 Vaults Available:", fg="cyan")
    for sigil, v in state["vaults"].items():
        click.echo(f"• {sigil}: {len(v.get('glyphs', []))} glyphs, {len(v.get('rituals', []))} rituals")
CODE

# glyphs.py
cat > glyphs.py <<CODE
from utils import catch_alchemy_errors
from vault import _load_state
import click
import json

@catch_alchemy_errors
def quote_all(scope="all", format="table"):
    state = _load_state()
    glyphs = []
    for vault in state.get("vaults", {}).values():
        glyphs.extend(vault.get("glyphs", []))
    if format == "json":
        print(json.dumps(glyphs, indent=2))
    elif format == "markdown":
        for g in glyphs:
            print(f"| {g['id']} | {g['name']} | {g['symbol']} | {g['type']} | {g['power']} |")
    else:
        click.secho("⚡ Glyphs (Table):", fg="cyan")
        for g in glyphs:
            click.echo(f"• {g['name']} ({g['symbol']}) → {g['type']} {g['power']}")
CODE

# rituals.py
cat > rituals.py <<CODE
from utils import catch_alchemy_errors
from vault import _load_state
import click

@catch_alchemy_errors
def list_rituals():
    state = _load_state()
    rituals = []
    for vault in state.get("vaults", {}).values():
        rituals.extend(vault.get("rituals", []))
    if not rituals:
        click.secho("📭 No rituals found.", fg="yellow")
    else:
        click.secho("🔮 Rituals Discovered:", fg="cyan")
        for r in rituals:
            click.echo(f"• {r.get('name')} → Pattern: {r.get('pattern')}")

@catch_alchemy_errors
def ritual():
    click.echo("🌀 Ritual execution not implemented.")
CODE

# share.py
cat > share.py <<CODE
import subprocess
def share_backend():
    subprocess.call(["ngrok", "http", "8000"])
CODE

# cli.py
cat > cli.py <<CODE
import click
from utils import catch_alchemy_errors, AlchemyError
from vault import bundle, ingest, list_vaults
from glyphs import quote_all
from rituals import list_rituals, ritual
from share import share_backend

@click.group()
def cli():
    pass

@cli.group()
def vault():
    pass

@vault.command("bundle")
@click.argument("sigil")
def bundle_vault(sigil):
    bundle(sigil)

@vault.command("ingest")
@click.argument("file", type=click.Path(exists=True))
def ingest_vault(file):
    ingest(file)

@vault.command("list")
def vault_list():
    list_vaults()

@cli.group()
def ritual():
    pass

@ritual.command("list")
def ritual_list():
    list_rituals()

@ritual.command("run")
def ritual_run():
    ritual()

@cli.group()
def glyph():
    pass

@glyph.command("quote")
@click.argument("scope", default="all")
@click.option("--format", default="table")
def quote(scope, format):
    quote_all(scope, format)

@cli.group()
def share():
    pass

@share.command("backend")
def backend():
    share_backend()
CODE

# main.py
cat > main.py <<CODE
#!/usr/bin/env python3
from cli import cli
if __name__ == "__main__":
    cli()
CODE

chmod +x main.py
sudo ln -sf "$PWD/main.py" /usr/local/bin/codex-alchemy
echo "✅ Done. Run 'codex-alchemy --help'"
