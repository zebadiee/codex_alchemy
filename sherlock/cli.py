import click
from sherlock.core import find_artifacts
from sherlock.web import watts0n_search

@click.command()
@click.argument('query', required=False)
@click.option('--path', default='~', help='Base directory to begin local search.')
def main(query, path):
    if not query:
        query = click.prompt('What artifact are you investigating?')
    click.echo(f"🔍 Searching locally for '{query}' in {path}...")
    local = find_artifacts(query, path)
    if local:
        click.echo("✅ Found locally:")
        for f in local:
            click.echo(f" - {f}")
    else:
        click.echo("❌ No local results. Escalate? (y/n)")
        if click.confirm('', default=True):
            click.echo("🌐 Searching web via Watts0n...")
            remote = watts0n_search(query)
            for item in remote:
                click.echo(f" - [{item['source']}] {item['title']}")

if __name__ == "__main__":
    main() 