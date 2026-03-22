from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import string
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    APP_NAME: str = "Bit.ly Pet Project"
    ENV: Literal["test", "dev", "prod"] = "dev"

    DB_DRIVER: str = "postgresql+asyncpg"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 6432
    DB_NAME: str = "postgres"

    RANDOM_SLUG_LENGTH: int = 6
    RANDOM_SLUG_CHARSET: str = string.ascii_letters + string.digits

    CUSTOM_SLUG_MIN_LENGTH: int = 2
    CUSTOM_SLUG_MAX_LENGTH: int = 32
    CUSTOM_SLUG_PATTERN: str = r"^[a-zA-Z0-9_-]+$"

    SLUG_EXPIRY_MIN_SECONDS: int = 60
    SLUG_EXPIRY_MAX_SECONDS: int = 365 * 24 * 3600
    SLUG_EXPIRY_DEFAULT_SECONDS: int | None = None

    REDIRECT_SLUG_MAX_LENGTH: int = 256
    URL_MAX_LENGTH: int | None = 256

    SCHEDULER_DELETE_EXPIRED_LINKS_INTERVAL_MINUTES: int = 60

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def IS_TEST(self) -> bool:
        return self.ENV == "test"

    @property
    def IS_DEV(self) -> bool:
        return self.ENV == "dev"


@lru_cache
def get_settings() -> Settings:
    return Settings()
