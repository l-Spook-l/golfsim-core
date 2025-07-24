from pydantic import BaseModel


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
