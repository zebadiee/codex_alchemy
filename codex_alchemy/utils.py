import click
from rich import print as rprint
from datetime import datetime
import hashlib
import json

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

def log(message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rprint(f"[{now}] {message}")

def hash_glyph(glyph_dict: dict) -> str:
    """Compute a deterministic hash for a glyph dict (excluding volatile keys)."""
    safe = {k: v for k, v in glyph_dict.items() if k not in ["timestamp", "id"]}
    serialized = json.dumps(safe, sort_keys=True)
    return hashlib.blake2b(serialized.encode(), digest_size=16).hexdigest()

