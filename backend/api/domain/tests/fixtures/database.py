from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from contextlib import contextmanager

from dependency_injector import providers
from api.data.src.db_models.Base import Base


@contextmanager
def get_test_db(client):
    engine_instance = create_engine(
        "sqlite+pysqlite:///:memory:",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_local_instance = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine_instance,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine_instance)

    with client.app.container.database.override_providers(
        engine=providers.Object(engine_instance),
        SessionLocal=providers.Object(session_local_instance),
    ) as db_container:
        yield db_container
