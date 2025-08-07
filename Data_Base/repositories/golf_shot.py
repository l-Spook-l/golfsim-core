from datetime import datetime, timedelta

from sqlalchemy import insert, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.repositories.base import BaseRepository
from data_base.models import GolfShot
from logging_config import logger


class GolfShotRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_new_shot(self, shot_result: dict):
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
    ):
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

    async def get_last_shot(self):
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
            return last_shot
        except Exception as error:
            logger.error(f"Error occurred while reading last data: {error}", exc_info=True)
            return None

    async def get_first_shot_date(self):
        try:
            query = select(GolfShot.date).order_by(GolfShot.date.asc()).limit(1)
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.error(f"Error occurred while reading first shot: {error}", exc_info=True)
            return None
