from pydantic import BaseModel, Field
from datetime import datetime


class GolfShotSchema(BaseModel):
    carry: float = Field(..., title="Carry (yd)")
    ball_speed: float = Field(..., title="Ball (mph)")
    angle_v: float = Field(..., title="Launch V")
    angle_h: float = Field(..., title="Launch H")

    model_config = {
        "from_attributes": True
    }


class GolfShotsSchema(BaseModel):
    id: int
    club: str = 'default_club'  # Значение по умолчанию
    ball_speed: float
    angle_v: float
    angle_h: float
    carry: float
    roll: float
    total: float
    lateral: float
    spin: float
    date: datetime

    def as_list(self) -> list[str]:
        return [
            str(self.id),
            self.club,
            str(self.ball_speed),
            str(self.angle_v),
            str(self.angle_h),
            str(self.carry),
            str(self.roll),
            str(self.total),
            str(self.lateral),
            str(self.spin),
            self.date.strftime("%Y-%m-%d %H:%M:%S"),
        ]


class HSVSettingSchema(BaseModel):
    profile_name: str = Field(max_length=15, description="Profile name (maximum 15 characters)")
    hue_min: int
    hue_max: int
    saturation_min: int
    saturation_max: int
    value_min: int
    value_max: int

    model_config = {
        "from_attributes": True  # Это замена orm_mode Для работы с SQLAlchemy
    }
