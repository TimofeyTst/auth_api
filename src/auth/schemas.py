# import re

# from pydantic import EmailStr, Field, validator

# STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


# class AuthUser(ORJSONModel):
#     email: EmailStr
#     password: str = Field(min_length=6, max_length=128)

#     @validator("password")
#     def valid_password(cls, password: str) -> str:
#         if not re.match(STRONG_PASSWORD_PATTERN, password):
#             raise ValueError(
#                 "Password must contain at least "
#                 "one lower character, "
#                 "one upper character, "
#                 "digit or "
#                 "special symbol"
#             )

#         return password

# TODO: Check if this should be integrated
# from typing import Any

# from src.auth.config import auth_config
# from src.config import settings


# def get_refresh_token_settings(
#     refresh_token: str,
#     expired: bool = False,
# ) -> dict[str, Any]:
#     base_cookie = {
#         "key": auth_config.REFRESH_TOKEN_KEY,
#         "httponly": True,
#         "samesite": "none",
#         "secure": auth_config.SECURE_COOKIES,
#         "domain": settings.SITE_DOMAIN,
#     }
#     if expired:
#         return base_cookie

#     return {
#         **base_cookie,
#         "value": refresh_token,
#         "max_age": auth_config.REFRESH_TOKEN_EXP,
#     }


import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
