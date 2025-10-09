from fastapi import APIRouter
from dependency_injector.wiring import inject

from api.api.src.containers.interactors import GetAllLessonsInteractorDep

router = APIRouter()


@router.get("/lessons")
@inject
async def get_all_lessons(interactor: GetAllLessonsInteractorDep):
    return interactor()
