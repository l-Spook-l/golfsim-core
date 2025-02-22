from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import GolfShot
from sqlalchemy.ext.asyncio import AsyncSession


class DataBase:
    @classmethod
    async def add_data(cls, speed_ball: [int, float], angle: [int, float], distance: [int, float],
                       session: AsyncSession) -> bool:
        try:
            stat = insert(GolfShot).values(speed=speed_ball, angle=angle, distance=distance)
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
    async def get_data(cls, session: AsyncSession):
        try:
            query = select(GolfShot).order_by(GolfShot.date.desc())
            res = await session.execute(query)
            return res.scalars().all()
        except Exception as error:
            print(f"Error occurred while reading data: {error}")
            return False
