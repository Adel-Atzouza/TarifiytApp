from typing import Any
from dependency_injector.wiring import inject

from api.domain.src.models.Lesson import Lesson

from api.api.src.containers.repositories import LessonsRepositoryLogicDep
from api.api.src.containers.repositories import FakeRepositoryLogicDep

class GetAllLessonsInteractor:
    @inject
    def __init__(self, lessonRepositoryLogic: LessonsRepositoryLogicDep, fakeRepositoryLogic: FakeRepositoryLogicDep) -> None:
        self.lessonRepositoryLogic = lessonRepositoryLogic
        self.fakeRepositoryLogic = fakeRepositoryLogic

    def __call__(self, *args: Any, **kwds: Any):
        return [self.lessonRepositoryLogic.get_all_lessons(), id(self.fakeRepositoryLogic.get_all_lessons())]
