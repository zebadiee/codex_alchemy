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
