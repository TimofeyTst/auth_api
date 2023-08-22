from typing import Any

from pydantic import PostgresDsn, root_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    @root_validator(skip_on_failure=True)
    def validate_sentry_non_local(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data["ENVIRONMENT"].is_deployed and not data["SENTRY_DSN"]:
            raise ValueError("Sentry is not set")

        return data


settings = Config()


app_configs: dict[str, Any] = {"title": "Auth API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
