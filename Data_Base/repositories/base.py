from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from data_base.config_db import Base
from core.logging_config import logger


class BaseRepository:
    """
    Base repository for database operations.

    Attributes:
        session (AsyncSession): Asynchronous SQLAlchemy session.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.MAX_PROFILES = 10

    async def delete_by_id(self, model: Type[Base], obj_id: int) -> bool:
        """
        Deletes an object from the database by its ID.

        Args:
            model (Type[Base]): SQLAlchemy model from which to delete the record.
            obj_id (int): Identifier of the object to delete.

        Returns:
            bool: True if deletion was successful, otherwise False.
        """
        try:
            query = delete(model).where(model.id == obj_id)
            await self.session.execute(query)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error while deleting from {e}")
            return False
