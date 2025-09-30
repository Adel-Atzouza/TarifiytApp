from abc import ABC, abstractmethod
from api.domain.src.models.Lesson import Lesson


class LessonsRepository(ABC):
    @abstractmethod
    def get_lesson_by_id(self, lesson_id: int) -> Lesson:
        ...

    def get_all_lessons(self) -> list[Lesson]:
        ...

    @abstractmethod
    def create_lesson(self, lesson: Lesson) -> Lesson:
        ...

    @abstractmethod
    def update_lesson(self, lesson_id: int, lesson: Lesson) -> Lesson:
        ...

    @abstractmethod
    def delete_lesson(self, lesson_id: int) -> None:
        ...