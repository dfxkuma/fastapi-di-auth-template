from typing import Dict, Any, List, TYPE_CHECKING
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise

if TYPE_CHECKING:
    from app.common.database.config import TortoiseConfig


class DatabaseManager:
    connection: Dict[str, Any]
    config: "TortoiseConfig"
    entities: List[str]

    @classmethod
    async def initialize(cls, app=None) -> None:
        config = generate_config(
            cls.connection["url"],
            app_modules={"models": cls.entities},
            testing=cls.connection.get("testing", False),
            connection_label=cls.connection.get("connection_label", "default"),
        )

        if app:
            await RegisterTortoise(
                app=app,
                config=config,
                generate_schemas=cls.config.generate_schemas,
                add_exception_handlers=cls.config.add_exception_handlers,
            )
        else:
            await Tortoise.init(config=config)
            if cls.config.generate_schemas:
                await Tortoise.generate_schemas()

    @classmethod
    async def close(cls) -> None:
        await Tortoise.close_connections()

    @classmethod
    def load(cls, app=None):
        from contextlib import asynccontextmanager
        from typing import AsyncGenerator

        @asynccontextmanager
        async def _load() -> AsyncGenerator[None, None]:
            await cls.initialize(app)
            yield
            await cls.close()

        return _load()
