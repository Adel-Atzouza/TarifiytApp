import os
from typing import Annotated, Iterator, Optional
from dependency_injector.wiring import Provide, Closing
from fastapi import Depends
from sqlalchemy import create_engine
from dependency_injector import containers, providers
from sqlalchemy.orm import Session, sessionmaker

from api.api.src import routers
from api.data.src import lessons

import logging
from contextvars import ContextVar, Token
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_URL = os.environ.get("DB_URL") or "sqlite+pysqlite:///:memory:"

# Add sqlite-specific connect args to allow usage in single-threaded test runs
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(
    url=DB_URL,
    pool_pre_ping=True,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Context var to hold the per-request Session
_SESSION_CTX: ContextVar[Optional[Session]] = ContextVar("_SESSION_CTX", default=None)

def set_request_session(session: Session) -> Token:
    return _SESSION_CTX.set(session)

def reset_request_session(token: Token) -> None:
    _SESSION_CTX.reset(token)

def get_current_session() -> Session:
    session = _SESSION_CTX.get()
    if session is None:
        raise RuntimeError("DB session not set for this request")
    return session

# Simple context manager for non-HTTP contexts (CLI, scripts)
@contextmanager
def session_context() -> Iterator[Session]:
    session = SessionLocal()
    token = set_request_session(session)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        reset_request_session(token)

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[lessons, routers]
    )
    # Provide current request-bound Session via context var
    session = providers.Callable(get_current_session)



SessionDep = Annotated[Session, Depends(Provide[Container.session])]