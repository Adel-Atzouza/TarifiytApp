from contextlib import AbstractContextManager
from typing import Callable
from typing_extensions import Annotated
from dependency_injector import containers, providers
from dotenv import dotenv_values
from sqlalchemy.orm import Session
from fastapi import Depends
from dependency_injector.wiring import Provide

from api.api.src.containers.database_factory import Database

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api"]
    )
    config_file = ".env"
    env_config = dotenv_values(config_file)

    db = providers.Singleton(Database, db_url=env_config["DB_URL"])
    session = providers.Factory(db.provided.session)

SessionDep = Annotated[Callable[[], AbstractContextManager[Session]], Depends(Provide[Container.session])]