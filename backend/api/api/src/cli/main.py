import typer
from rich.console import Console

from api.api.src.containers.container import Container

app = typer.Typer()
container = Container()
console = Console()

@app.command()
def get_lessons() -> None:
    interactor = container.interactors.get_all_lessons_interactor()
    results = interactor()

    console.print(f"Found {len(results)} lessons:")
    for result in results:
        console.print(f"- {result.model_dump()}")


if __name__ == "__main__":
    typer.run(get_lessons)
