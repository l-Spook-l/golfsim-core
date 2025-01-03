from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .config_db import Base


class GolfShot(Base):
    __tablename__ = 'user_settings_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    speed: Mapped[float]
    angle: Mapped[float]
    # angle_horizontal: Mapped[float]
    distance: Mapped[int]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # user: Mapped[int]
    # DK021_2015: Mapped[str]
    # Status: Mapped[str]
    # Procurement_type: Mapped[str]
    # Region: Mapped[str]
    # Dispatch_time: Mapped[str]
    # Email: Mapped[str]
    # created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
