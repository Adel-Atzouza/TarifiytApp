from api.data.src.db_models.LessonDB import LessonDB
from api.domain.src.models.Lesson import Lesson


class LessonDBMapper:
    @staticmethod
    def to_db_model(lesson):
        return LessonDB(
            id=lesson.id, title=lesson.title, description=lesson.description
        )

    @staticmethod
    def to_domain_model(lesson_db):
        return Lesson(
            id=lesson_db.id, title=lesson_db.title, description=lesson_db.description
        )
