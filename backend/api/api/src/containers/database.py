from contextlib import AbstractContextManager
from typing import Callable
import os
from typing_extensions import Annotated
from dependency_injector import containers, providers
from sqlalchemy.orm import Session
from fastapi import Depends
from dependency_injector.wiring import Provide

from api.api.src.containers.database_factory import Database

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api"]
    )

    db_url = os.environ.get("DB_URL", "mysql+pymysql://root:password@db:3306/tarifiyt")
    db = providers.Singleton(Database, db_url=db_url)
    session = providers.Factory(db.provided.session)

SessionDep = Annotated[Callable[[], AbstractContextManager[Session]], Depends(Provide[Container.session])]