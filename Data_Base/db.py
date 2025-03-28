import logging
from datetime import datetime

from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from .config_db import Base
from .models import GolfShot

logger = logging.getLogger(__name__)


class DataBase:
    MAX_PROFILES = 10  # Максимальное количество профилей

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
    async def save_hsv_or_pixel_value(cls, session: AsyncSession, model: type[Base], value: dict) -> bool:
        try:
            # Проверяем, сколько уже записей в БД
            result = await session.execute(select(model))
            count = len(result.scalars().all())

            if count >= cls.MAX_PROFILES:
                logger.warning(f"Достигнут лимит в {cls.MAX_PROFILES} профилей {model}, запись не добавлена")
                return False  # Отказ в добавлении

            # Вставляем новую запись
            stat = insert(model).values(**value)
            await session.execute(stat)
            await session.commit()

            await cls.set_active_profile(session, model, value['profile_name'])

            logger.info(f"Новая запись {model} успешно сохранена")
            return True
        except Exception as error:
            logger.error(f"Error occurred save {model} data: {error}", exc_info=True)
            return False

    @classmethod
    async def set_active_profile(cls, session: AsyncSession, model: type[Base], profile_name: str) -> bool:
        try:
            # Сначала устанавливаем все профили как неактивные
            await session.execute(update(model).values(is_active=False))
            # Устанавливаем новый профиль как активный
            await session.execute(
                update(model).where(model.profile_name == profile_name).values(is_active=True))
            await session.commit()
            return True
        except Exception as error:
            logger.error(f"Error occurred save PixelDistance data: {error}", exc_info=True)
            return False

    @classmethod
    async def get_active_profile(cls, session: AsyncSession, model: type[Base]):
        try:
            query = (
                select(model).where(model.is_active is True).limit(1)
            )
            active_profile = await session.execute(query)
            logger.info(f"Получен активный профиль {model}")
            return active_profile.scalars().fetchall()  # Вернем объект GolfShot
        except Exception as error:
            logger.error(f"Error occurred get active profile: {error}", exc_info=True)
            return None

    @classmethod
    async def delete_record(cls, session: AsyncSession, model: type[Base], record_id: int):
        """Удаляет запись из указанной модели по ID."""
        try:
            # query = select().filter(model.id == record_id).one()
            # record = await session.execute(query)
            query = delete(model).where(model.id == record_id)
            await session.execute(query)
            await session.commit()
            print(f"Запись с ID {record_id} удалена из {model.__tablename__}")
        except NoResultFound:
            print(f"Запись с ID {record_id} не найдена в {model.__tablename__}")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при удалении из {model.__tablename__}: {e}")
