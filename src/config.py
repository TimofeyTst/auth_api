from typing import Any

from pydantic import FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    @field_validator("SENTRY_DSN")
    def validate_sentry_non_local(cls, value: str, info: FieldValidationInfo):
        environment = info.data.get("ENVIRONMENT")
        if environment and environment.is_deployed and not value:
            raise ValueError("Sentry is not set")
        return value


settings = Config()


app_configs: dict[str, Any] = {"title": "Auth API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
