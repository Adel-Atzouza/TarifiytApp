from api.api.src.containers.container import Container
from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from api.api.src.containers.interactors import GetAllLessonsInteractorDep
from api.domain.src.models.Lesson import Lesson
from api.domain.src.interactors.get_all_lessons_interactor import GetAllLessonsInteractor

router = APIRouter()

@router.get("/lessons")
@inject
async def get_all_lessons(
    interactor: Annotated[GetAllLessonsInteractor, Depends(Provide[Container.interactors.get_all_lessons_interactor])]
) -> list[Lesson]:
    return interactor()
