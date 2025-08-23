from sqlalchemy import insert, select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.repositories.base import BaseRepository
from data_base.models import HSVSetting
from core.logging_config import logger
from core.exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError


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

    async def get_inactive_hsv_sets(self):
        query = select(HSVSetting).where(HSVSetting.is_active.is_(False))
        result = await self.session.execute(query)
        # all() или .fetchall()
        return result.scalars().all()