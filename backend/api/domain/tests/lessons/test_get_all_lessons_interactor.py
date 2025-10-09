
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from dependency_injector import providers
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from api.domain.tests.fixtures.factories import LessonFactory
from api.api.src.tarifiyt_http import TarifiytHTTP as app
from api.domain.src.mappers.lesson_db_mapper import LessonDBMapper
from api.domain.tests.fixtures.database import get_test_db
from api.data.src.lessons.lessons_repository_logic import LessonsRepositoryLogic
from api.api.src.containers.repositories import LessonsRepositoryLogicDep
from api.api.src.containers.database import session_context
from api.data.src.db_models.Base import Base


class TestGetLessonsEndpoint:
    @pytest.fixture
    def client(self):
        test_app = app()
        with TestClient(test_app) as client:
            yield client

    def test_get_all_lessons(self, client):
        response_value = [
            LessonFactory.build(id="1", title="Test Lesson 1"),
            LessonFactory.build(id="2", title="Test Lesson 2"),
        ]


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


class TestGetAllLessonsInteractor:
    @pytest.fixture
    def client(self):
        test_app = app()
        with TestClient(test_app) as client:
            yield client

    def test_get_all_lessons_interactor(self, client):
        response_value = [
            LessonFactory.build(id="1", title="Test Lesson 1"),
            LessonFactory.build(id="2", title="Test Lesson 2"),
        ]

        class MockRepository:
            def get_all_lessons(self, *args, **kwds):
                return response_value


        result = client.app.container.interactors.get_all_lessons_interactor(lessonRepositoryLogic=MockRepository())()
        assert result == response_value


class TestLessonsRepositoryLogic:
    @pytest.fixture
    def client(self):
        test_app = app()
        with TestClient(test_app) as client:
            yield client

    def test_lessons_repository_logic(self, client):
        response_value = [
            LessonFactory.build(id="1", title="Test Lesson 1"),
            LessonFactory.build(id="2", title="Test Lesson 2"),
        ]

        with get_test_db(client) as db_container:
            session_local_instance = db_container.SessionLocal()
            
            response_value_db = [LessonDBMapper.to_db_model(x) for x in response_value]
            with session_local_instance() as session:
                session.add_all(response_value_db)
                session.commit()

                lessons_repository_logic = client.app.container.repositories.lessons_repository_logic(session=session)
                result = lessons_repository_logic.get_all_lessons()
                assert result == response_value