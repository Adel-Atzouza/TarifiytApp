from dependency_injector import containers, providers

from .repositories import Container as RepositoriesContainer
from .interactors import Container as InteractorsContainer
from .database import Container as DatabaseContainer

from api.data import src as repositories
from api.domain.src import interactors

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[repositories, interactors]
    )

    interactors = providers.Container(InteractorsContainer)
    database = providers.Container(DatabaseContainer)
    repositories = providers.Container(RepositoriesContainer)