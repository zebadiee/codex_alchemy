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
