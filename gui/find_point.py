import flet as ft
import flet.canvas as cv

from data_base.config_db import async_session_maker
from data_base.repositories.pixel_distance import PixelDistanceSettingRepository
from logging_config import logger


class PixelDistanceCalibrator:
    def __init__(self):
        self.image_path = "media_files_for_tests/video_dnerp/ball 240 2024-07-27 141246.png"
        self.shapes = []
        self.distance_px_value = 0
        self.coordinates_text = ft.Text("Coordinates: (0, 0)")
        self.distance_cm_text = ft.Text("1 cm = 0 px")
        self.canvas = cv.Canvas(expand=True)
        self.tab_content = ft.Row()

    async def add_hsv_value(self, e):
        if self.distance_px_value > 0:
            async with async_session_maker() as session:
                repo = PixelDistanceSettingRepository(session)
                success = await repo.add_new_pixel_distance_set({
                    'pixels_per_cm': self.distance_px_value,
                    'profile_name': 'test 1'
                })
                logger.info("Data added successfully" if success else "Failed to add data")
        else:
            logger.info("Try again, please")

    def on_click(self, e):
        x, y = int(e.local_x), int(e.local_y)

        if len(self.shapes) >= 2:
            self.shapes.clear()

        self.shapes.append(cv.Circle(x, y, 8, paint=ft.Paint(color=ft.Colors.GREEN)))
        self.canvas.shapes = self.shapes
        self.canvas.update()

        self.coordinates_text.value = f"Coordinates: ({x}, {y})"
        if len(self.shapes) > 1:
            coords = [(circle.x, circle.y) for circle in self.shapes]
            self.distance_px_value = abs(coords[0][0] - coords[1][0])
            self.distance_cm_text.value = f"1 cm = {self.distance_px_value} px"
        self.tab_content.update()

    def build_section(self):
        image = ft.Image(src=self.image_path)
        stack = ft.Stack([image, self.canvas])
        gd = ft.GestureDetector(on_tap_up=self.on_click, content=stack)
        save_button = ft.ElevatedButton(text="Save values", on_click=self.add_hsv_value)

        self.tab_content = ft.Row([
            ft.Column([self.coordinates_text, self.distance_cm_text, save_button]),
            gd
        ])

        return self.tab_content
