from api.fixtures.factories import lessons
from api.fixtures.app import client as AppClient
from api.fixtures.database import get_test_db
from api.domain.src.mappers.lesson_db_mapper import LessonDBMapper


class TestGetLessonsEndpoint:
    def test_get_all_lessons(self):
        response_value = lessons
        client = next(AppClient())

        with get_test_db(client) as db_container:
            session_local_instance = db_container.SessionLocal()

            response_value_db = [LessonDBMapper.to_db_model(x) for x in response_value]
            with session_local_instance() as session:
                session.add_all(response_value_db)
                session.commit()

                response = client.get("/lessons")
                assert response.status_code == 200
                data = response.json()
                assert data == [obj.model_dump() for obj in response_value]
