from api.fixtures.app import client as AppClient
from api.fixtures.factories import lessons


class TestGetAllLessonsInteractor:
    def test_get_all_lessons_interactor(self):
        response_value = lessons

        class MockRepository:
            def get_all_lessons(self, *args, **kwds):
                return response_value

        client = next(AppClient())
        result = client.app.container.interactors.get_all_lessons_interactor(  # type: ignore
            lessonRepositoryLogic=MockRepository()
        )()
        assert result == response_value
