from fastapi.params import Depends
from typing_extensions import Annotated
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from api.domain.src.interactors.get_all_lessons_interactor import GetAllLessonsInteractor

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api.api.src.routers"]
    )
    get_all_lessons_interactor = providers.Factory(GetAllLessonsInteractor)

GetAllLessonsInteractorDep = Annotated[GetAllLessonsInteractor, Depends(Provide[Container.get_all_lessons_interactor])]
