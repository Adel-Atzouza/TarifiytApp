from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from api.api.src.containers.interactors import GetAllLessonsInteractorDep
from api.domain.src.models.Lesson import Lesson

router = APIRouter()

@router.get("/lessons")
@inject
async def get_all_lessons(
    interactor: GetAllLessonsInteractorDep
):
    return interactor()
