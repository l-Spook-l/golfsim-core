from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .config_db import Base


class GolfShot(Base):
    __tablename__ = 'user_settings_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    club: Mapped[str] = mapped_column(String(length=25), nullable=True)
    ball_speed: Mapped[float] = mapped_column(nullable=False, default=0.0)
    angle_v: Mapped[float] = mapped_column(nullable=False, default=0.0)
    angle_h: Mapped[float] = mapped_column(nullable=False, default=0.0)
    carry: Mapped[float] = mapped_column(nullable=False, default=0.0)
    roll: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total: Mapped[float] = mapped_column(nullable=False, default=0.0)
    lateral: Mapped[float] = mapped_column(nullable=False, default=0.0)
    spin: Mapped[int] = mapped_column(nullable=False, default=0)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)


    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # user: Mapped[int]
    # DK021_2015: Mapped[str]
    # Status: Mapped[str]
    # Procurement_type: Mapped[str]
    # Region: Mapped[str]
    # Dispatch_time: Mapped[str]
    # Email: Mapped[str]
    # created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())


class HSVSetting(Base):
    __tablename__ = 'hsv_settings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_name: Mapped[str] = mapped_column(String(length=99), nullable=False, unique=True)
    hue_min: Mapped[int]
    hue_max: Mapped[int]
    saturation_min: Mapped[int]
    saturation_max: Mapped[int]
    value_min: Mapped[int]
    value_max: Mapped[int]
    is_active: Mapped[bool]


class PixelDistance(Base):
    __tablename__ = 'pixel_distance'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_name: Mapped[str] = mapped_column(String(length=99), nullable=False, unique=True)
    pixels_per_cm: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool]
