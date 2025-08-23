from sqlalchemy import insert, select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.repositories.base import BaseRepository
from data_base.models import PixelDistance
from core.logging_config import logger
from core.exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError


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
