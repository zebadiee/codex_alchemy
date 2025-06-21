# codex_view.py — Terminal-based Glyph Visualizer

from rich.console import Console
from rich.table import Table
from rich import box
from vault import Vault

console = Console()

vault = Vault()
glyphs = vault.restore()

if not glyphs:
    console.print("[bold red]No glyphs found in vault.[/bold red]")
    exit(1)

# Create table
console.print("\n[bold cyan]📜 Codex Glyph Vault[/bold cyan]\n")
table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
table.add_column("#", width=3)
table.add_column("Name", style="bold")
table.add_column("Hash", width=18)
table.add_column("Vector Preview", overflow="fold")

for idx, g in enumerate(glyphs):
    preview = ", ".join(f"{v:.2f}" for v in g.vector[:4]) + ("..." if len(g.vector) > 4 else "")
    table.add_row(
        str(idx+1),
        g.name,
        vault._hash(g),
        preview
    )

console.print(table)
console.print(f"\n[green]Total glyphs:[/green] {len(glyphs)}")

