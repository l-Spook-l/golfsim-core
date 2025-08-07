import os
import json

import aiofiles
from logging_config import logger


async def load_settings() -> dict:
    data = {}
    if os.path.exists("settings.json"):
        async with aiofiles.open("settings.json", "r", encoding="utf-8") as f:
            try:
                content = await f.read()
                if content.strip():  # Проверка на пустоту
                    data = json.loads(content)
                else:
                    logger.info("Файл пустой. Создаём заново.")
            except json.JSONDecodeError:
                logger.info("Файл повреждён. Создаём заново.")

    return data


class ShotSettingsSingleton:
    _instance = None
    __selected_club = {"selected_club": "Driver"}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def selected_club(self):
        return self.__selected_club

    @selected_club.setter
    def selected_club(self, value: dict):
        self.__selected_club = value


class ShotResult:
    def __init__(self, filename="data/last_shot_result.json"):
        self.settings = ShotSettingsSingleton()
        self.filename = filename
        self.shot_data = {
            "club": "",
            "speed": 0.0,
            "carry": 0.0,
            "angle_v": 0,
            "angle_h": 0
        }
        self._load_result_data()

    def _load_result_data(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                content = json.load(file)
                self.shot_data.update(content)

    @property
    def speed(self) -> float:
        return self.shot_data["speed"]

    @speed.setter
    def speed(self, value: float):
        self.shot_data["speed"] = value

    @property
    def vertical_angle(self) -> int:
        return self.shot_data["angle_v"]

    @vertical_angle.setter
    def vertical_angle(self, angle: int = 0):
        self.shot_data["angle_v"] = angle

    @property
    def horizontal_angle(self) -> int:
        return self.shot_data["angle_h"]

    @horizontal_angle.setter
    def horizontal_angle(self, angle: int = 0):
        self.shot_data["angle_h"] = angle

    @property
    def carry(self) -> float:
        return self.shot_data["carry"]

    @carry.setter
    def carry(self, value: float):
        self.shot_data["carry"] = value

    def save_data(self) -> None:
        self.shot_data["club"] = self.settings.selected_club["selected_club"]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.shot_data, file, indent=4)


class SelectClub:
    def __init__(self, filename: str = "data/selected_club.json"):
        self.settings = ShotSettingsSingleton()  # shared state
        self.filename = filename

    @property
    def club(self) -> str:
        return self.settings.selected_club["selected_club"]

    @club.setter
    def club(self, club: str):
        self.settings.selected_club["selected_club"] = club

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.settings.selected_club, file, indent=4)
