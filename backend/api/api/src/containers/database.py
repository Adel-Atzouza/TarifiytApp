from contextlib import AbstractContextManager
from typing import Callable
import os
from typing_extensions import Annotated
from dependency_injector import containers, providers
from sqlalchemy.orm import Session
from fastapi import Depends
from dependency_injector.wiring import Provide

from api.data import src as repositories
from api.api.src.containers.database_factory import Database

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[repositories]
    )

    db_url = os.environ.get("DB_URL")
    db = providers.Singleton(Database, db_url=db_url)
    session = providers.Factory(db.provided.session)

SessionDep = Annotated[Callable[[], AbstractContextManager[Session]], Depends(Provide[Container.session])]