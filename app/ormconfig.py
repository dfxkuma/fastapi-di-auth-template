from app.common.database import (
    DatabaseManager,
    DataSource,
    TortoiseConfig,
)
from app.common.utils.env_validator import get_settings

settings = get_settings()


class DatabaseLoader(DatabaseManager):
    connection = DataSource.Postgres(
        uri=settings.DATABASE_URI, testing=settings.APP_ENV == "development"
    )
    config = TortoiseConfig(
        generate_schemas=True,
        add_exception_handlers=True,
    )
    entities = ["app.hello.entities.message", "app.members.entities"]
