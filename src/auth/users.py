import re
import uuid
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
    exceptions,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    RedisStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx_oauth.clients.google import GoogleOAuth2

from src.auth.config import auth_config
from src.auth.schemas import UserCreate
from src.database import User, get_user_db
from src.redis import redis_client

SECRET = auth_config.JWT_SECRET
STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


google_oauth_client = GoogleOAuth2(
    auth_config.GOOGLE_OAUTH_CLIENT_ID, auth_config.GOOGLE_OAUTH_CLIENT_SECRET
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    reset_password_token_lifetime_seconds = auth_config.RESET_PASSWORD_TOKEN_EXP
    verification_token_secret = SECRET
    verification_token_lifetime_seconds = auth_config.VERIFY_TOKEN_EXP

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise InvalidPasswordException(
                reason="Password must contain at least one lower character, one upper character, digit or special symbol"
            )

        await self.validate_username(user.username)

    async def validate_username(self, username: str):
        user = await self.user_db.get_user_by_username(username)

        if user is not None:
            raise exceptions.UserAlreadyExists()

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has reset their password.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis_client, lifetime_seconds=auth_config.AUTH_TOKEN_EXP)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
