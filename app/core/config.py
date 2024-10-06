import redis

from typing_extensions import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str]
    BACKEND_CORS: List[str]
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 8025
    SMTP_FROM_ADDRESS: str = "default@mai.com"
    SMTP_FROM_PASSWORD: Optional[str | None] = None

    SQL_PASSWORD: str
    SQL_USER: str
    SQL_DB: str
    SQL_HOST: str
    SQL_PORT: int = 5432

    TEST_SQL_PASSWORD: str
    TEST_SQL_USER: str
    TEST_SQL_DB: str
    TEST_SQL_HOST: str
    TEST_SQL_PORT: int = 5432

    @property
    def ASYNC_DB_URI(self):
        return f"postgresql+asyncpg://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_HOST}:{self.SQL_PORT}/{self.SQL_DB}"

    @property
    def TEST_ASYNC_DB_URI(self):
        return f"postgresql+asyncpg://{self.TEST_SQL_USER}:{self.TEST_SQL_PASSWORD}@{self.TEST_SQL_HOST}:{self.TEST_SQL_PORT}/{self.TEST_SQL_DB}"

    @property
    def SYNC_DB_URI(self):
        return f"postgresql+psycopg://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_HOST}:{self.SQL_PORT}/{self.SQL_DB}"

    @property
    def REDIS_URI(self):
        return redis.Redis(
            host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True
        )

    REDIS_PORT: int = 6379
    REDIS_HOST: str = "localhost"

    RABBITMQ_PASSWORD: str
    RABBITMQ_USER: str
    RABBITMQ_PORT: int = 5672
    RABBITMQ_HOST: str = "localhost"

    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    REQUESTS_LOGGIN_MIDDLEWARE: bool = False


settings = Settings()  # type: ignore
