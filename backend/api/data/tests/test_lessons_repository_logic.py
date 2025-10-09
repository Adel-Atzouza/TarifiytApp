from api.fixtures.factories import lessons
from api.fixtures.app import client as AppClient
from api.fixtures.database import get_test_db
from api.domain.src.mappers.lesson_db_mapper import LessonDBMapper


class TestGetLessonsRepositoryLogic:
    def test_lessons_repository_logic(self):
        response_value = lessons
        client = next(AppClient())

        with get_test_db(client) as db_container:
            session_local_instance = db_container.SessionLocal()

            response_value_db = [LessonDBMapper.to_db_model(x) for x in response_value]
            with session_local_instance() as session:
                session.add_all(response_value_db)
                session.commit()

                lessons_repository_logic = (
                    client.app.container.repositories.lessons_repository_logic(  # type: ignore
                        session=session
                    )
                )
                result = lessons_repository_logic.get_all_lessons()
                assert result == response_value
