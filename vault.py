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
