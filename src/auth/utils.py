from typing import Optional

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import UP
from sqlalchemy import select


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_user_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)
