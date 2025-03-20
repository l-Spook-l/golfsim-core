import logging
from datetime import datetime

from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from .config_db import Base
from .models import GolfShot, HSVSetting, PixelDistance

logger = logging.getLogger(__name__)


class DataBase:
    @classmethod
    async def add_data(cls, shot_result: dict, session: AsyncSession) -> bool:

        try:
            print("dqweqweqw", GolfShot(**shot_result))
            stat = insert(GolfShot).values(**shot_result)
            await session.execute(stat)
            await session.commit()
            return True
        except Exception as error:
            print(f"Error occurred while adding data: {error}")
            return False

    @classmethod
    async def get_last_shot(cls, session: AsyncSession):
        query = (
            select(GolfShot.carry, GolfShot.ball_speed, GolfShot.angle_v, GolfShot.angle_h)
            .order_by(GolfShot.date.desc())
            .limit(1)
        )
        result = await session.execute(query)
        last_shot = tuple(str(item) for item in result.fetchone())
        return last_shot  # Вернем объект GolfShot

    @classmethod
    async def get_data(cls, session: AsyncSession, start_date: datetime = None, end_date: datetime = None):
        # golf_club_name = f"%{golf_club_name}%"
        # golf_club_name, limit
        try:
            query = select(GolfShot)

            if start_date and end_date:
                query = query.where(GolfShot.date >= start_date, GolfShot.date <= end_date)

            query = query.order_by(GolfShot.date.desc())
            res = await session.execute(query)

            return res.scalars().fetchall()
        except Exception as error:
            logger.error(f"Error occurred while reading data: {error}", exc_info=True)
            return None

    @classmethod
    async def save_hsv_value(cls, session: AsyncSession, hsv_value: dict) -> bool:
        try:
            print("HSVSetting(**hsv_value) - ", HSVSetting(**hsv_value))
            stat = insert(HSVSetting).values(**hsv_value)
            await session.execute(stat)
            await session.commit()
            return True
        except Exception as error:
            logger.error(f"Error occurred save hsv data: {error}", exc_info=True)
            return False
