from datetime import datetime
from typing import Type

from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.config_db import Base
from data_base.models import GolfShot, HSVSetting, PixelDistance
from logging_config import logger
from exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.MAX_PROFILES = 10

    async def delete_by_id(self, model: Type[Base], obj_id):
        try:
            query = delete(model).where(model.id == obj_id)
            await self.session.execute(query)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при удалении из  {e}")
            return False


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

    async def get_all_shots(self, start_date: datetime = None, end_date: datetime = None):
        try:
            query = select(GolfShot)
            if start_date and end_date:
                query = query.where(GolfShot.date >= start_date, GolfShot.date <= end_date)

            query = query.order_by(GolfShot.date.desc())
            # TODO: add filter by name golf_club
            # if golf_club:
            #     query = query.filter(GolfShot.golf_club.ilike(golf_club_name))
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


class HSVSettingRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_new_hsv_set(self, data: dict):
        try:
            count_records = await self.session.scalar(select(func.count()).select_from(HSVSetting))
            if count_records >= self.MAX_PROFILES:
                logger.warning(f"Profile limit of {self.MAX_PROFILES} reached for HSVSetting, record not added")
                raise ProfileLimitReachedError()

            stat = insert(HSVSetting).values(**data).returning(HSVSetting.id)
            result = await self.session.execute(stat)
            new_id = result.scalar_one()
            await self.session.commit()
            await self.set_active_hsv_set(new_id)
            return True
        except ProfileLimitReachedError:
            raise
        except IntegrityError:
            await self.session.rollback()
            raise ProfileNameAlreadyExistsError()
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred save add_new_hsv_set data: {error}", exc_info=True)
            return False

    async def set_active_hsv_set(self, hsv_id: int):
        try:
            await self.session.execute(update(HSVSetting).values(is_active=False))
            await self.session.execute(update(HSVSetting).where(HSVSetting.id == hsv_id).values(is_active=True))
            await self.session.commit()
            return True
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred save active profile: {error}", exc_info=True)
            return False

    async def get_active_hsv_set(self):
        try:
            query = select(HSVSetting).where(HSVSetting.is_active).limit(1)
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.error(f"Error occurred get active profile: {error}", exc_info=True)
            return None

    async def get_all_hsv_set(self):
        query = select(HSVSetting)
        result = await self.session.execute(query)
        # all() или .fetchall()
        return result.scalars().all()


class PixelDistanceSettingRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_new_pixel_distance_set(self, data: dict):
        try:
            count_records = await self.session.scalar(select(func.count()).select_from(PixelDistance))
            if count_records >= self.MAX_PROFILES:
                logger.warning(f"Profile limit of {self.MAX_PROFILES} reached , record not added")
                raise ProfileLimitReachedError()
            stat = insert(PixelDistance).values(**data).returning(PixelDistance.id)
            result = await self.session.execute(stat)
            new_id = result.scalar_one()
            await self.session.commit()
            await self.set_active_pixel_distance_set(new_id)
            return True
        except ProfileLimitReachedError:
            raise
        except IntegrityError:
            await self.session.rollback()
            raise ProfileNameAlreadyExistsError()
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred save new pixel distance data: {error}", exc_info=True)
            return False

    async def set_active_pixel_distance_set(self, pix_dis_id: int):
        try:
            await self.session.execute(update(PixelDistance).values(is_active=False))
            await self.session.execute(update(PixelDistance).where(PixelDistance.id == pix_dis_id).values(is_active=True))
            await self.session.commit()
            return True
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred save active profile: {error}", exc_info=True)
            return False

    async def get_active_pixel_distance_set(self):
        try:
            query = select(PixelDistance).where(PixelDistance.is_active).limit(1)
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.error(f"Error occurred get active profile: {error}", exc_info=True)
            return None
