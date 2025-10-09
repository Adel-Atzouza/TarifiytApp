from fastapi.testclient import TestClient
from api.api.src.tarifiyt_http import TarifiytHTTP as app


def client():
    test_app = app()
    with TestClient(test_app) as client:
        yield client


# def client():
#     return TestClient(app())
