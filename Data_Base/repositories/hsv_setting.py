import os
from typing import Optional, Sequence

import aiofiles
import aiohttp
from sqlalchemy import insert, select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.repositories.base import BaseRepository
from data_base.models import HSVSetting
from core.logging_config import logger
from core.exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError


class HSVSettingRepository(BaseRepository):
    """
    Repository for managing HSV profile settings.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_default_hsv(self) -> HSVSetting:
        """
        Creates a default HSV profile and loads an image.

        Returns:
            HSVSetting: Saved default profile model.
        """
        url = "https://coffective.com/wp-content/uploads/2018/06/default-featured-image.png.jpg"
        new_folder = "mobile_uploads/images/profile_images/"
        local_path = os.path.join(new_folder, "default.jpg")

        async with aiohttp.ClientSession() as client:
            async with client.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(local_path, mode='wb') as f:
                        await f.write(await resp.read())

        default_hsv_data = HSVSetting(
            profile_name="default",
            hue_min=0,
            hue_max=180,
            saturation_min=0,
            saturation_max=255,
            value_min=0,
            value_max=255,
            is_active=True,
            photo=f"{new_folder}default.jpg",
        )
        self.session.add(default_hsv_data)
        await self.session.commit()
        return default_hsv_data

    async def add_new_hsv_set(self, data: dict) -> bool:
        """
        Adds a new HSV profile. Activates it after adding.

        Args:
            data (dict): Profile data.

        Raises:
            ProfileLimitReachedError: Profile limit exceeded.
            ProfileNameAlreadyExistsError: A profile with this name already exists.

        Returns:
            bool: True if successful, otherwise False.
        """
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

    async def set_active_hsv_set(self, hsv_id: int) -> bool:
        """
        Sets the profile by ID as active, deactivating the others.

        Args:
            hsv_id (int): ID of the profile to activate.

        Returns:
            bool: True if successful.
        """
        try:
            await self.session.execute(update(HSVSetting).values(is_active=False))
            await self.session.execute(update(HSVSetting).where(HSVSetting.id == hsv_id).values(is_active=True))
            await self.session.commit()
            return True
        except Exception as error:
            await self.session.rollback()
            logger.error(f"Error occurred save active profile: {error}", exc_info=True)
            return False

    async def get_active_hsv_set(self) -> Optional[HSVSetting]:
        """
        Retrieves the active HSV profile.

        Returns:
            HSVSetting | None: Active profile, if found.
        """
        try:
            query = select(HSVSetting).where(HSVSetting.is_active).limit(1)
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.error(f"Error occurred get active profile: {error}", exc_info=True)
            return None

    async def get_inactive_hsv_sets(self) -> Sequence[HSVSetting]:
        """
        Retrieves a list of all inactive HSV profiles.

        Returns:
            Sequence[HSVSetting]: Inactive profiles.
        """
        try:
            query = select(HSVSetting).where(HSVSetting.is_active.is_(False))
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as error:
            logger.error(f"Error while retrieving inactive HSV profiles: {error}", exc_info=True)
            return []
