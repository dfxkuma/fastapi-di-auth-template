from typing import Literal, Optional, Type
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["get_settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_ENV: Literal["development", "production", "testing"]
    SERVER_PORT: int
    DATABASE_URI: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    JWT_SECRET_KEY: str

    @staticmethod
    @field_validator("SERVER_PORT")
    def check_port_range(value: int):
        if not 0 < value < 65536:
            raise ValueError("SERVER_PORT number must be between 1 and 65535")
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()
