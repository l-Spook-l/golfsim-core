from pydantic import BaseModel, Field


class GolfShotSchema(BaseModel):
    carry: float = Field(..., title="Carry (yd)")
    ball_speed: float = Field(..., title="Ball (mph)")
    angle_v: float = Field(..., title="Launch V")
    angle_h: float = Field(..., title="Launch H")

    model_config = {
        "from_attributes": True
    }


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
