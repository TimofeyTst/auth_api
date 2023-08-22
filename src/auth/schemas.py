import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    username: Optional[str] = Field(..., min_length=1)


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = Field(None, min_length=1)
