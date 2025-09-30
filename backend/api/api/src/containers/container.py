from dependency_injector import containers, providers

from .repositories import Container as RepositoriesContainer
from .interactors import Container as InteractorsContainer
from .database import Container as DatabaseContainer

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api.domain.src.interactors", "api.api.src.routers"]
    )

    interactors = providers.Container(InteractorsContainer)
    database = providers.Container(DatabaseContainer)
    repositories = providers.Container(RepositoriesContainer)