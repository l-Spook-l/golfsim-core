import flet as ft

from ui.components.find_color import FindBallByColor
from ui.components.find_point import PixelDistanceCalibrator
from ui.components.general_settings import GeneralSettings


class SettingsView:
    def __init__(self):
        self.tabs = ft.Tabs()
        self.content_container = ft.Container()
        self.settings = ft.Container()
        self.current_tab = None
        self.load_general_settings_section = GeneralSettings()
        self.load_find_ball_color_section = FindBallByColor()
        self.load_find_distance_point = PixelDistanceCalibrator()

    async def on_tab_change(self, e):
        match self.tabs.selected_index:
            case 0:
                self.current_tab = await self.load_general_settings_section.build_section()
            case 1:
                self.current_tab = await self.load_find_ball_color_section.build_section()
            case 2:
                self.current_tab = self.load_find_distance_point.build_section()

        self.content_container.content = self.current_tab
        self.content_container.update()

    async def init(self) -> ft.Container:
        self.tabs = ft.Tabs(
            selected_index=0,
            on_change=self.on_tab_change,
            tabs=[
                ft.Tab(text="General settings"),
                ft.Tab(text="Find ball's color"),
                ft.Tab(text="Find pixel distance on screen"),
            ],
        )

        self.content_container = ft.Container(
            content=await self.load_general_settings_section.build_section(),
        )

        self.settings = ft.Container(
            content=ft.Column(
                [
                    self.tabs,
                    self.content_container
                ]
            )
        )
        return self.settings
