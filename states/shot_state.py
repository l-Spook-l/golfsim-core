import json
from enum import Enum
from pathlib import Path

from logging_config import logger


class AngleType(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ShotState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data_dir="data"):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.file_last_shot = Path(data_dir) / "last_shot_result.json"
        self.file_selected_club = Path(data_dir) / "selected_club.json"
        self.file_clubs_info = Path(data_dir) / "clubs_info.json"

        # состояние в памяти
        self.golf_clubs = {}
        self.selected_club = "Driver"
        self.selected_angle_type = AngleType.VERTICAL
        self.shot_data = {
            "club": self.selected_club,
            "speed": 0.0,
            "carry": 0.0,
            "angle_v": 0.0,
            "angle_h": "0.0",
        }

        self._load_last_shot()
        self._load_clubs_info()
        self._initialized = True

    def _load_last_shot(self):
        if self.file_last_shot.exists():
            try:
                with open(self.file_last_shot, "r", encoding="utf-8") as f:
                    self.shot_data.update(json.load(f))
            except json.JSONDecodeError:
                logger.error("last_shot_result.json is corrupted! Using default data.")
            except OSError as e:
                logger.error(f"Failed to read last_shot_result.json: {e}")
        else:
            logger.warning("last_shot_result.json is missing. Using default values.")

    def _load_clubs_info(self):
        if self.file_clubs_info.exists():
            try:
                with open(self.file_clubs_info, "r", encoding="utf-8") as file:
                    self.golf_clubs = json.load(file)
            except json.JSONDecodeError:
                logger.error("clubs_info.json is corrupted! Club data not loaded.")
            except OSError as e:
                logger.error(f"Failed to read clubs_info.json: {e}")
        else:
            logger.error("clubs_info.json is missing! Clubs not loaded.")

    def save(self):
        # сохраняем выбранный клуб
        with open(self.file_selected_club, "w", encoding="utf-8") as f:
            json.dump({"selected_club": self.selected_club}, f, indent=4)

        # сохраняем результат
        self.shot_data["club"] = self.selected_club
        with open(self.file_last_shot, "w", encoding="utf-8") as f:
            json.dump(self.shot_data, f, indent=4)

    @property
    def angle_type(self):
        return self.selected_angle_type

    @angle_type.setter
    def angle_type(self, angle_type):
        self.selected_angle_type = angle_type

    @property
    def speed(self) -> float:
        return self.shot_data["speed"]

    @speed.setter
    def speed(self, value: float):
        self.shot_data["speed"] = value

    @property
    def carry(self) -> float:
        return self.shot_data["carry"]

    @carry.setter
    def carry(self, value: float):
        self.shot_data["carry"] = value

    @property
    def vertical_angle(self) -> int:
        return self.shot_data["angle_v"]

    @vertical_angle.setter
    def vertical_angle(self, angle: int):
        self.shot_data["angle_v"] = angle

    @property
    def horizontal_angle(self) -> int:
        return self.shot_data["angle_h"]

    @horizontal_angle.setter
    def horizontal_angle(self, angle: int):
        self.shot_data["angle_h"] = angle

    @property
    def club(self) -> str:
        return self.selected_club

    @club.setter
    def club(self, club: str):
        self.selected_club = club
