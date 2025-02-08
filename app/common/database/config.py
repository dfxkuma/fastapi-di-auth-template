from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TortoiseConfig:
    generate_schemas: bool = True
    add_exception_handlers: bool = True
    use_tz: bool = False
    timezone: str = "UTC"


def _datasource_common_config(uri: str, testing: bool = False) -> Dict[str, Any]:
    return {"url": uri, "testing": testing, "connection_label": "models"}


class DataSource:
    Postgres = _datasource_common_config
    MySQL = _datasource_common_config
