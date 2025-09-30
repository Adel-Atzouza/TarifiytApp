from dependency_injector.wiring import inject

from api.domain.src.repositories.lessons_repository import LessonsRepository
from api.api.src.containers.database import SessionDep
from api.data.src.db_models.LessonDB import LessonDB
from api.domain.src.mappers.lesson_db_mapper import LessonDBMapper

class LessonsRepositoryLogic(LessonsRepository):
    @inject
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_lesson_by_id(self, lesson_id: int):
        with self.session() as session:
            lesson = session.query(LessonDB).filter(LessonDB.id == lesson_id).first()
            return LessonDBMapper.to_domain_model(lesson)
    
    def get_all_lessons(self):
        with self.session() as session:
            lessons = session.query(LessonDB).all()
            return [LessonDBMapper.to_domain_model(lesson) for lesson in lessons]

    def create_lesson(self, lesson):
        with self.session() as session:
            db_lesson = LessonDBMapper.to_db_model(lesson)
            session.add(db_lesson)
            session.commit()
            session.refresh(db_lesson)
            return LessonDBMapper.to_domain_model(db_lesson)

    def update_lesson(self, lesson_id: int, lesson):
        with self.session() as session:
            existing_lesson = session.query(LessonDB).filter(LessonDB.id == lesson_id).first()
            if existing_lesson:
                existing_lesson.title = lesson.title
                existing_lesson.description = lesson.description

                session.commit()
                session.refresh(existing_lesson)
                return LessonDBMapper.to_domain_model(existing_lesson)
        raise ValueError("Lesson not found")

    def delete_lesson(self, lesson_id: int):
        with self.session() as session:
            existing_lesson = session.query(LessonDB).filter(LessonDB.id == lesson_id).first()
            if existing_lesson:
                session.delete(existing_lesson)
                session.commit()
                return
        raise ValueError("Lesson not found")