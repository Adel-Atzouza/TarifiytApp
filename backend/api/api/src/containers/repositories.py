from dependency_injector import containers, providers
from typing import Annotated
from fastapi import Depends
from dependency_injector.wiring import Provide

from api.data.src.lessons.lessons_repository_logic import LessonsRepositoryLogic

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api"]
    )
    lessons_repository_logic = providers.Factory(LessonsRepositoryLogic)
    
LessonsRepositoryLogicDep = Annotated[LessonsRepositoryLogic, Depends(Provide[Container.lessons_repository_logic])]
