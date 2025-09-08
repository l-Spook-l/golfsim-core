from pydantic import BaseModel, Field
from datetime import datetime


class LastGolfShotSchema(BaseModel):
    """
    Schema for representing the last shot.

    Used in the API to provide key shot parameters:
    - Carry (flight distance)
    - Ball speed
    - Launch V/H (launch angles)
    """
    carry: float = Field(..., title="Carry (yd)")
    ball_speed: float = Field(..., title="Ball (mph)")
    angle_v: float = Field(..., title="Launch V")
    angle_h: str = Field(..., title="Launch H")

    model_config = {
        "from_attributes": True
    }


class GolfShotsSchema(BaseModel):
    """
    Full shot description schema.

    Used when returning a list of shots or a single shot from the database.
    """
    id: int
    club: str
    ball_speed: float
    angle_v: float
    angle_h: str
    carry: float
    roll: float
    total: float
    lateral: str
    spin: int
    date: datetime

    def as_list(self) -> list[str]:
        """
        Represents shot data as a list of strings.
        Convenient for export (e.g., to a table).
        """
        return [
            str(self.id),
            self.club,
            str(self.ball_speed),
            str(self.angle_v),
            self.angle_h,
            str(self.carry),
            str(self.roll),
            str(self.total),
            self.lateral,
            str(self.spin),
            self.date.strftime("%Y-%m-%d %H:%M:%S"),
        ]


class HSVSettingSchema(BaseModel):
    """
    HSV profile settings schema.

    Used for input validation and API representation when working with filters.
    """
    profile_name: str = Field(min_length=1, max_length=15, description="Profile name (maximum 15 characters)")
    hue_min: int
    hue_max: int
    saturation_min: int
    saturation_max: int
    value_min: int
    value_max: int

    model_config = {
        "from_attributes": True
    }
