from datetime import datetime

from sqlalchemy import insert, select
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

    async def get_all_shots(self, start_date: datetime = None, end_date: datetime = None, club: str = ""):
        try:
            query = select(GolfShot)
            if start_date and end_date:
                query = query.where(GolfShot.date >= start_date, GolfShot.date <= end_date)
            if club:
                query = query.where(GolfShot.club == club)

            query = query.order_by(GolfShot.date.desc())

            result = await self.session.execute(query)
            # total_count = await session.scalar(
            #     select(func.count())
            #     .select_from(Workout)
            #     .filter(GolfShot.is_public)
            #     .filter(GolfShot.name.ilike(query_name) if name else True)
            #     .filter(GolfShot.difficulty.in_(difficulty) if difficulty else True)
            # )

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