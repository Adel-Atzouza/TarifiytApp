from api.domain.src.models.Lesson import Lesson
from polyfactory.factories.pydantic_factory import ModelFactory


class LessonFactory(ModelFactory[Lesson]): ...


lessons = [
    LessonFactory.build(id="1", title="Test Lesson 1"),
    LessonFactory.build(id="2", title="Test Lesson 2"),
]
