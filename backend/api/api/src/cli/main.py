import typer
from rich.console import Console
from dependency_injector import providers

from api.api.src.containers.container import Container
from api.api.src.containers.database import session_context

app = typer.Typer()
console = Console()
container = Container()

@app.command()
def get_lessons() -> None:
    with session_context():
        interactor = container.interactors.get_all_lessons_interactor()
        results = interactor()

        console.print(f"Results: {results}")


if __name__ == "__main__":
    typer.run(get_lessons)
