import json
from pathlib import Path


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

        # состояние в памяти
        self.selected_club = "Driver"
        self.shot_data = {
            "club": self.selected_club,
            "speed": 0.0,
            "carry": 0.0,
            "angle_v": 0,
            "angle_h": 0
        }

        self._load()
        self._initialized = True

    def _load(self):
        if self.file_last_shot.exists():
            try:
                with open(self.file_last_shot, "r", encoding="utf-8") as f:
                    self.shot_data.update(json.load(f))
            except Exception:
                pass

        # синхронизация
        self.shot_data["club"] = self.selected_club

    def save(self):
        # сохраняем выбранный клуб
        with open(self.file_selected_club, "w", encoding="utf-8") as f:
            json.dump({"selected_club": self.selected_club}, f, indent=4)

        # сохраняем результат
        self.shot_data["club"] = self.selected_club
        with open(self.file_last_shot, "w", encoding="utf-8") as f:
            json.dump(self.shot_data, f, indent=4)

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
