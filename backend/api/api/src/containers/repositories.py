from dependency_injector import containers, providers
from typing import Annotated
from fastapi import Depends
from dependency_injector.wiring import Provide

from api.domain.src import interactors
from api.data.src.lessons.lessons_repository_logic import LessonsRepositoryLogic
from api.data.src.lessons.fake_repository import FakeRepositoryLogic

from .database import Container as DatabaseContainer

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[interactors]
    )

    lessons_repository_logic = providers.Factory(LessonsRepositoryLogic)
    fake_repository_logic = providers.Factory(FakeRepositoryLogic)

LessonsRepositoryLogicDep = Annotated[LessonsRepositoryLogic, Depends(Provide[Container.lessons_repository_logic])]
FakeRepositoryLogicDep = Annotated[FakeRepositoryLogic, Depends(Provide[Container.fake_repository_logic])]
