# codex_alchemy/assistant.py
import json
import click
from vault import _load_state
from utils import catch_alchemy_errors

@click.group()
def assistant():
    """🧠 Codex Alchemy Assistant — your symbolic co-pilot."""
    pass

@assistant.command("status")
@catch_alchemy_errors
def show_status():
    """📦 Summarize current vault, glyph, and ritual status."""
    state = _load_state()
    vaults = state.get("vaults", {})
    if not vaults:
        click.secho("📭 No vaults found.", fg="yellow")
        return
    click.secho("📦 Vault Summary:", fg="cyan")
    for sigil, v in vaults.items():
        glyphs = len(v.get("glyphs", []))
        rituals = len(v.get("rituals", []))
        click.echo(f"• {sigil} → {glyphs} glyphs, {rituals} rituals")

@assistant.command("suggest")
@click.argument("topic", required=False)
@catch_alchemy_errors
def suggest_ritual(topic):
    """🔮 Suggest rituals based on topic or current state."""
    state = _load_state()
    rituals = []
    for v in state.get("vaults", {}).values():
        rituals.extend(v.get("rituals", []))
    if not rituals:
        click.secho("🧠 No rituals available for suggestion.", fg="yellow")
        return
    click.secho("🔮 Ritual Suggestions:", fg="green")
    for r in rituals:
        if topic and topic.lower() not in r["name"].lower():
            continue
        click.echo(f"• {r['name']} → Pattern: {r['pattern']}")

@assistant.command("ritual-boost")
@click.option("--glyph", required=True, help="Name of the glyph to boost")
@click.option("--intensity", default="medium", type=click.Choice(["low", "medium", "high"]), help="Boost intensity level")
@catch_alchemy_errors
def ritual_boost(glyph, intensity):
    """⚡ Simulate symbolic ritual boost for a glyph."""
    levels = {"low": 1, "medium": 2, "high": 3}
    power_up = levels.get(intensity, 2)
    click.secho("🌀 Ritual Boost Initiated", fg="cyan")
    click.echo(f"• Glyph: {glyph}")
    click.echo(f"• Intensity: {intensity.capitalize()} ({'🔹'*power_up})")
    click.echo(f"✨ Boosting symbolic resonance... done.")
    click.secho(f"✅ Ritual successfully amplified '{glyph}' by x{power_up} intensity.", fg="green")

# Register assistant in cli.py (append to cli.py bottom):
# from assistant import assistant
# cli.add_command(assistant, name="assist")

