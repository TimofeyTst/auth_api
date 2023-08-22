from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_SECRET: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str

    # EXP in seconds
    AUTH_TOKEN_EXP: int = 60 * 60 * 24 * 365  # 365 days
    RESET_PASSWORD_TOKEN_EXP: int = 300  # 5 minutes
    VERIFY_TOKEN_EXP: int = 3600  # 1 hour


auth_config = AuthConfig()
