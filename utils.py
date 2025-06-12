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
