from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Mutual"
    environment: str = "development"
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/mutual")
    jwt_secret: str = Field(default="change-me")
    jwt_algorithm: str = Field(default="HS256")
    jwt_audience: str | None = None
    jwt_issuer: str | None = None
    auto_create_tables: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
