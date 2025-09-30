from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api.src.routers.lessons import router as lessons_router
from api.api.src.containers.container import Container



class TarifiytHTTP(FastAPI):
    def __init__(self) -> None:
        super().__init__()

        self.container = Container()

        self._setup_cors_middlewares()
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
