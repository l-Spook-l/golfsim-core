from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import insert, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.repositories.base import BaseRepository
from data_base.models import GolfShot
from core.logging_config import logger


class GolfShotRepository(BaseRepository):
    """
    Repository for working with golf shot data (GolfShot).
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_new_shot(self, shot_result: dict) -> bool:
        """
        Adds a new shot to the database.

        Args:
            shot_result (dict): Shot data (keys should correspond to the columns of the GolfShot model).

        Returns:
            bool: True if the addition was successful, otherwise False.
        """
        try:
            new_data = insert(GolfShot).values(**shot_result)
            await self.session.execute(new_data)
            await self.session.commit()
            return True
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred while adding data: {error}")
            return False

    async def get_all_shots(
            self,
            start_date: datetime = None,
            end_date: datetime = None,
            club: str = None,
            sort_by: str = "date",
            sort_desc: bool = True,
            limit_records: int = 10
    ) -> Sequence[GolfShot]:
        """
        Retrieves a list of shots with filtering and sorting options.

        Args:
            start_date (datetime, optional): Start date for filtering.
            end_date (datetime, optional): End date for filtering.
            club (str, optional): Filter by club type.
            sort_by (str): Field to sort by (default is 'date').
            sort_desc (bool): Sort in descending order (default is True).
            limit_records (int): Maximum number of records (default is 10).

        Returns:
            Sequence[GolfShot]: List of GolfShot objects.
        """
        try:
            query = select(GolfShot)
            if start_date and end_date:
                query = query.where(GolfShot.date >= start_date, GolfShot.date < (end_date + timedelta(days=1)))
            if club:
                query = query.where(GolfShot.club == club)

            sort_column = getattr(GolfShot, sort_by)
            query = query.order_by(desc(sort_column) if sort_desc else asc(sort_column))
            query = query.limit(limit_records)
            result = await self.session.execute(query)
            return result.scalars().fetchall()
        except Exception as error:
            logger.error(f"Error occurred while reading data: {error}", exc_info=True)
            return []

    async def get_last_shot(self) -> dict | None:
        """
        Retrieves the data of the last shot.

        Returns:
            dict | None: The last shot as a dictionary, or None if no data is available.
        """
        try:
            query = (
                select(GolfShot.carry, GolfShot.ball_speed, GolfShot.angle_v, GolfShot.angle_h)
                .order_by(GolfShot.date.desc())
                .limit(1)
            )
            result = await self.session.execute(query)
            last_shot = result.mappings().fetchone()
            if last_shot is None:
                return {
                    "carry": 0.0,
                    "ball_speed": 0.0,
                    "angle_v": 0.0,
                    "angle_h": 0.0,
                }
            return dict(last_shot)
        except Exception as error:
            logger.error(f"Error occurred while reading last data: {error}", exc_info=True)
            return None

    async def get_first_shot_date(self) -> datetime | None:
        """
        Retrieves the date of the very first shot.

        Returns:
            datetime | None: Date of the first shot, or None if no data is available.
        """
        try:
            query = select(GolfShot.date).order_by(GolfShot.date.asc()).limit(1)
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.error(f"Error occurred while reading first shot: {error}", exc_info=True)
            return None
