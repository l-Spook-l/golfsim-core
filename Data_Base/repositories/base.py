from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from data_base.config_db import Base
from logging_config import logger


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.MAX_PROFILES = 10

    async def delete_by_id(self, model: Type[Base], obj_id) -> bool:
        try:
            query = delete(model).where(model.id == obj_id)
            await self.session.execute(query)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error while deleting from {e}")
            return False
