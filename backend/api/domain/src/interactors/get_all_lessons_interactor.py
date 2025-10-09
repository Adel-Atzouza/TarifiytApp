from typing import Any
from dependency_injector.wiring import inject


from api.api.src.containers.repositories import LessonsRepositoryLogicDep


class GetAllLessonsInteractor:
    @inject
    def __init__(self, lessonRepositoryLogic: LessonsRepositoryLogicDep) -> None:
        self.lessonRepositoryLogic = lessonRepositoryLogic

    def __call__(self, *args: Any, **kwds: Any):
        return self.lessonRepositoryLogic.get_all_lessons()
