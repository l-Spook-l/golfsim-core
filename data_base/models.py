from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data_base.config_db import Base


class GolfShot(Base):
    __tablename__ = 'drive_range_shots'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    club: Mapped[str] = mapped_column(String(length=25), nullable=True)
    ball_speed: Mapped[float] = mapped_column(nullable=False, default=0.0)
    angle_v: Mapped[float] = mapped_column(nullable=False, default=0.0)
    angle_h: Mapped[str] = mapped_column(String(length=8), nullable=False, default="0.0")
    carry: Mapped[float] = mapped_column(nullable=False, default=0.0)
    roll: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total: Mapped[float] = mapped_column(nullable=False, default=0.0)
    lateral: Mapped[str] = mapped_column(String(length=8), nullable=False, default="0.0")
    spin: Mapped[int] = mapped_column(nullable=False, default=0)
    date: Mapped[datetime] = mapped_column(default=datetime.now)


class HSVSetting(Base):
    __tablename__ = 'hsv_settings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_name: Mapped[str] = mapped_column(String(length=20), nullable=False, unique=True)
    hue_min: Mapped[int]
    hue_max: Mapped[int]
    saturation_min: Mapped[int]
    saturation_max: Mapped[int]
    value_min: Mapped[int]
    photo: Mapped[str | None]
    value_max: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=False)


class PixelDistance(Base):
    __tablename__ = 'pixel_distance'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_name: Mapped[str] = mapped_column(String(length=20), nullable=False, unique=True)
    pixels_per_cm: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
