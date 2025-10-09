from fastapi import APIRouter
from dependency_injector.wiring import inject

from api.api.src.containers.interactors import GetAllLessonsInteractorDep
from api.domain.src.models.Lesson import Lesson

router = APIRouter()


@router.get("/lessons")
@inject
async def get_all_lessons(interactor: GetAllLessonsInteractorDep) -> list[Lesson]:
    return interactor()
