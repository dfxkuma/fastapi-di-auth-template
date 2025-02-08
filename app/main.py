from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.logger import service_logger
from app.common.utils.env_validator import get_settings
from app.containers import AppContainers
from app.ormconfig import DatabaseLoader

from app.hello.endpoints import router as hello_router
from app.auth.endpoints import router as auth_router

logger = service_logger("bootstrapper")
settings = get_settings()


def bootstrap() -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting application")

        application.container = container

        container.wire(
            modules=[
                __name__,
                "app.hello.endpoints",
                "app.auth.endpoints",
            ]
        )
        logger.info("Container Wiring complete")
        async with DatabaseLoader.load(app):
            logger.info("Tortoise ORM registered")
            yield
        logger.info("Shutting down application")
        logger.info("Tortoise ORM connections closed")
        logger.info("Application shutdown complete")

    app = FastAPI(
        title="FooBar Backend API",
        lifespan=lifespan,
        docs_url="/api-docs",
        redoc_url=None,
        debug=settings.APP_ENV == "development",
    )
    return app


container = AppContainers()
server = bootstrap()

server.include_router(auth_router)
server.include_router(hello_router)
