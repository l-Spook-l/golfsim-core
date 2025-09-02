import asyncio
import datetime
import json

import cv2
import cvzone
import aiofiles

from states.shot_state import ShotState, AngleType
from data_base.schemas import HSVSettingSchema
from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from data_base.repositories.hsv_setting import HSVSettingRepository
from core.find_angle import AngleCalculator
from shot_analysis.parser_flightscope import ParserFlightscope
from core.logging_config import logger
from core.config import myColorFinder, FRAMES_IN_SECOND, MIN_AREA


class HSVSettingsManager:
    @staticmethod
    async def get_active_hsv() -> dict:
        key_mapping = {
            "hmin": "hue_min",
            "smin": "saturation_min",
            "vmin": "value_min",
            "hmax": "hue_max",
            "smax": "saturation_max",
            "vmax": "value_max",
        }

        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            orm_obj = await repo.get_active_hsv_set()
            hsv_dict = HSVSettingSchema.model_validate(orm_obj).model_dump()

        return {new: hsv_dict[old] for new, old in key_mapping.items()}


class ShotDataManager:
    @staticmethod
    async def save_shot(shot_result: dict):
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            await repo.add_new_shot(shot_result)

    @staticmethod
    async def get_spin_for_club(club: str) -> int:
        async with aiofiles.open("data/clubs_info.json", "r", encoding='utf-8') as file:
            clubs = await file.read()
            clubs_data = json.loads(clubs)
            return clubs_data.get(club).get("spin_rate_average")


class GolfBallTracker:
    def __init__(self, hsv_vals, frame_time):
        self.hsv_vals = hsv_vals
        self.frame_time = frame_time
        self.angle_calculator = AngleCalculator()
        self.shot_state = ShotState()
        self.reset()

    def reset(self):  # мб поменять название
        self.pos_list = []
        self.list_counter = 1
        self.counter = -1
        self.distance_pix_x = 0
        self.distance_pix_y = 0
        self.distance_cm_x = 0
        self.distance_cm_y = 0
        self.distance_list_x = []
        self.distance_list_y = []
        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 0
        self.coordinates_angle = []
        self.len_pos_list = 0
        self.frame_count = 0
        self.seconds = 0

    def process_frame(self, frame):
        self.frame_count += 1
        self.seconds += self.frame_time
        img_color, mask = myColorFinder.update(frame, self.hsv_vals)
        img_contours, contours, width, high, area = cvzone.findContours(frame, mask, minArea=MIN_AREA)

        if contours:
            self._update_positions(contours[0]['center'])
        else:
            if len(self.pos_list) > 100:
                return self._finalize_shot()

        return None

    def _update_positions(self, center):
        if center not in self.pos_list:
            self.pos_list.append(center)
            self.counter += 1

        if len(self.pos_list) > self.len_pos_list:
            self.len_pos_list = len(self.pos_list)
            self.distance_pix_x += self.pos_list[self.counter][0] - self.pos_list[self.counter - 1][0]
            self.distance_pix_y += self.pos_list[self.counter - 1][1] - self.pos_list[self.counter][1]

            self.distance_cm_x = self.distance_pix_x / 30
            self.distance_cm_y = self.distance_pix_y / 30

            self.distance_list_x.append(self.distance_cm_x)
            self.distance_list_y.append(self.distance_cm_y)

            self.speed_x = ((self.distance_cm_x - self.distance_list_x[len(self.distance_list_x) - 2]) / self.frame_time) / 100
            self.speed_y = ((self.distance_cm_y - self.distance_list_y[len(self.distance_list_y) - 2]) / self.frame_time) / 100
            self.speed = ((self.speed_x ** 2) + (self.speed_y ** 2)) ** 0.5

            if self.speed > self.max_speed:
                self.max_speed = round(self.speed, 2)

    def _finalize_shot(self):
        self.coordinates_angle = [self.pos_list[7], self.pos_list[-1], [self.pos_list[-1][0], self.pos_list[7][1]]]
        angle = self.angle_calculator.get_angle(self.coordinates_angle)
        club = self.shot_state.club
        if self.shot_state.angle_type == AngleType.HORIZONTAL and angle != 0:
            angle = f"{angle} L" if angle > 0 else f"{abs(angle)} R"
        return {
            "max_speed": self.max_speed,
            "angle_v": angle if self.shot_state.angle_type == AngleType.VERTICAL
            else self.shot_state.golf_clubs.get(self.shot_state.club).get("launch_angle_average"),
            "angle_h": angle if self.shot_state.angle_type == AngleType.HORIZONTAL else 0.0,
            "club": club
        }


class ShotAnalyzer:
    def __init__(self, tracker: GolfBallTracker, data_manager: ShotDataManager):
        self.tracker = tracker
        self.data_manager = data_manager

    async def analyze_and_save(self, shot_data):
        spin = await self.data_manager.get_spin_for_club(shot_data["club"])
        if (shot_data["max_speed"] * 2.237 >= 45) and (5 <= shot_data["angle_v"] <= 45) and shot_data["angle_h"] <= 45:  # !!!!!!угол то строка!!
            result = await ParserFlightscope.get_shot_result(
                shot_data["max_speed"] * 2.237,
                shot_data["angle_v"],
                shot_data["angle_h"],
                spin
            )
        else:
            result = {
                "ball_speed": shot_data["max_speed"],
                "angle_v": shot_data["angle_v"],
                "angle_h": shot_data["angle_h"],
                "spin": spin
            }
        result["club"] = shot_data["club"]

        await self.data_manager.save_shot(result)
        self.tracker.shot_state.speed = shot_data["max_speed"]
        self.tracker.shot_state.vertical_angle = shot_data["angle_v"]
        self.tracker.shot_state.horizontal_angle = shot_data["angle_h"]
        self.tracker.shot_state.save()
        self.tracker.reset()


class VideoProcessor:
    def __init__(self, name_video_file: str):
        self.video_path = f'mobile_uploads/golf_shots/{name_video_file}'

    async def run(self):
        cap = cv2.VideoCapture(self.video_path)

        hsv_manager = HSVSettingsManager()
        hsv_vals = await hsv_manager.get_active_hsv()
        frame_time = FRAMES_IN_SECOND["FPS_240"]
        data_manager = ShotDataManager()
        tracker = GolfBallTracker(hsv_vals, frame_time)
        analyzer = ShotAnalyzer(tracker, data_manager)

        now = datetime.datetime.now()
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                shot_data = tracker.process_frame(frame)
                if shot_data:
                    await analyzer.analyze_and_save(shot_data)
        finally:
            cap.release()
            logger.info(f'time {datetime.datetime.now() - now}')


if __name__ == "__main__":
    asyncio.run(VideoProcessor("example.mp4").run())
