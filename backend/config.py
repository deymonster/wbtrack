from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    ENVIRONMENT: str = "local"

    # App

    DEBUG: bool = False
    WEB_CONCURRENCY: int = 1
    APP_SECRET_KEY: str
    APP_PORT: int = 8000
    ALLOW_ORIGINS: list[str]
    ALLOW_ORIGIN_REGEX: str

    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int

    # Telegram
    TELEGRAM_BOT_TOKEN: str



    # Wildberries

    WILDBERRIES_BASE_PATH: str
    AUTH_BASE_PATH: str
    WB_BASIC_TOKEN: str


    # PVZ Client
    AUTH_BASE_PATH: str
    DISCOVERY_URL: str
    S_POINT_URL: str
    POINT_RATING_URL: str
    POINT_BALANCE_URL: str

    # Redis

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_PASSWORD: str | None = None

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        if self.ENVIRONMENT in ["production", "docker"]:
            host = self.REDIS_HOST
        else:
            host = "localhost"

        if self.REDIS_PASSWORD:
            # URL-кодируем пароль для безопасного использования в URL
            encoded_password = quote_plus(self.REDIS_PASSWORD)
            return f"redis://:{encoded_password}@{host}:{self.REDIS_PORT}/0"
        return f"redis://{host}:{self.REDIS_PORT}/0"
        # return str(
        #     RedisDsn.build(  # type: ignore
        #         scheme="redis",
        #         username="default",
        #         password=self.REDIS_PASSWORD,
        #         host=host,
        #         port=int(self.REDIS_PORT),
        #     )
        # )

    # Postgres

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    POSTGRES_POOL_SIZE: int = 80
    POSTGRES_MAX_OVERFLOW: int = 10

    @computed_field
    @property
    def POSTGRES_POOL_SIZE_BY_SERVER(self) -> int:
        return self.POSTGRES_POOL_SIZE // self.WEB_CONCURRENCY



    @computed_field
    @property
    def DB_ASYNC_CONNECTION_STR(self) -> str:
        if self.ENVIRONMENT in ["production", "docker"]:
            host = self.POSTGRES_HOST
        else:
            host = "localhost"

        # URL-кодируем параметры для безопасного использования в URL
        username = quote_plus(self.POSTGRES_USER)
        password = quote_plus(self.POSTGRES_PASSWORD)
        database = quote_plus(self.POSTGRES_DB)

        return f"postgresql+asyncpg://{username}:{password}@{host}:{self.POSTGRES_PORT}/{database}"


settings = Settings()  # type: ignore


__all__ = [
    "settings",
]
