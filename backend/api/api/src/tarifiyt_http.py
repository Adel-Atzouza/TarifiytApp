from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.api.src.routers.lessons import router as lessons_router
from api.api.src.containers.container import Container
from api.api.src.containers.database import set_request_session, reset_request_session


class TarifiytHTTP(FastAPI):
    def __init__(self) -> None:
        super().__init__()

        self._setup_cors_middlewares()
        self._setup_di()
        self._setup_routers()

    def _setup_cors_middlewares(self) -> None:
        self.add_middleware(
            CORSMiddleware,
            # allow_origins=[
            #     str(origin) for origin in self._settings.backend_cors_origins
            # ],
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routers(self) -> None:
        self.include_router(lessons_router)

    def _setup_di(self) -> None:
        # Initialize container and install request-scope middleware
        container = Container()
        # Store on app state for potential debug/extension
        self.container: Container = container
        # Wire container according to its wiring_config so Provide[...] works
        container.wire()

        @self.middleware("http")
        async def di_request_scope_middleware(request: Request, call_next):
            session = self.container.database.SessionLocal()()
            token = set_request_session(session)
            try:
                response = await call_next(request)
                return response
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
                reset_request_session(token)
