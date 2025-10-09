import typer
from rich.console import Console

from api.api.src.containers.container import Container
from api.api.src.containers.database import session_context
from sqlalchemy.exc import OperationalError
from functools import wraps

app = typer.Typer()
console = Console()
container = Container()


def command(*c_args, **c_kwargs):
    def decorator(func):
        @app.command(*c_args, **c_kwargs)
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                with session_context():
                    return func(*args, **kwargs)
            except OperationalError:
                console.print("[red]Database is not reachable.[/red]")
                console.print(
                    "Tip: Start Docker (DB service) with: [bold]docker compose up -d[/bold], or set DB_URL to a reachable database."
                )
                raise typer.Exit(code=1)

        return wrapped

    return decorator


@command()
def get_lessons() -> None:
    interactor = container.interactors.get_all_lessons_interactor()
    results = interactor()

    console.print(f"Results: {results}")


if __name__ == "__main__":
    typer.run(get_lessons)
