from sqlalchemy import select
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from api.domain.src.repositories.lessons_repository import LessonsRepository
from api.api.src.containers.database import SessionDep

from api.data.src.db_models.LessonDB import LessonDB
from api.domain.src.mappers.lesson_db_mapper import LessonDBMapper

class FakeRepositoryLogic(LessonsRepository):
    @inject
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_lesson_by_id(self, lesson_id: int):
        lesson = self.session.query(LessonDB).filter(LessonDB.id == lesson_id).first()
        return LessonDBMapper.to_domain_model(lesson)

    def get_all_lessons(self): # type: ignore
        return self.session
    
    def create_lesson(self, lesson):
        db_lesson = LessonDBMapper.to_db_model(lesson)
        self.session.add(db_lesson)
        self.session.commit()
        self.session.refresh(db_lesson)
        return LessonDBMapper.to_domain_model(db_lesson)
    
    def update_lesson(self, lesson_id: int, lesson):
        db_lesson = self.session.get(LessonDB, lesson_id)
        if not db_lesson:
            raise ValueError(f"Lesson with id {lesson_id} not found")
        for key, value in lesson.dict().items():
            setattr(db_lesson, key, value)
        self.session.add(db_lesson)
        self.session.refresh(db_lesson)
        return LessonDBMapper.to_domain_model(db_lesson)
    
    def delete_lesson(self, lesson_id: int):
        db_lesson = self.session.get(LessonDB, lesson_id)
        if not db_lesson:
            raise ValueError(f"Lesson with id {lesson_id} not found")
        self.session.delete(db_lesson)
        return None

