import asyncio

import flet as ft

from gui.drive_range_section import DriveRangeSection
from logging_config import logger
from data_base.repositories.golf_shot import GolfShotRepository
from data_base.config_db import async_session_maker
from utils import SelectClub


class HomeView:
    def __init__(self):
        self.home_page = ft.Container()
        self.current_section = ft.Container()
        self.current_section_name = {"name": ""}
        self.latest_shot_data = None
        self.drive_range_section = None
        self.button_return_home = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.load_home_page())
        self.selected_club = SelectClub()

    async def init(self) -> ft.Container:
        """Initialize the view, load the latest shot data and the default section UI."""
        self.latest_shot_data = await self.last_shot()
        load_drive_range_section = DriveRangeSection(self.latest_shot_data)
        self.drive_range_section = await load_drive_range_section.build_section()

        self.home_page = ft.Container(
            content=ft.Row(
                controls=[
                    self.build_card("drive-range", "menu/drive-range.png"),
                    self.build_card("putting", "menu/putting.png"),
                    self.build_card("play-course", "menu/play-course.png"),
                ],
                expand=True,
                spacing=0
            ),
            expand=True
        )

        self.current_section.content = self.home_page
        asyncio.ensure_future(self.check_db_updates())
        return self.current_section

    def build_card(self, section_name: str, image_url: str) -> ft.Container:
        return ft.Container(
            content=ft.Image(src=image_url, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
            alignment=ft.alignment.center,
            expand=True,
            margin=10,
            ink=True,
            on_click=lambda e: self.update_section(section_name)
        )

    def update_section(self, section_name: str) -> None:
        self.current_section_name["name"] = section_name
        match section_name:
            case "drive-range":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("Drive range", size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    self.drive_range_section
                ])
                self.selected_club.club = "Driver"
            case "putting":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("🎯 Putting view")
                    ]),
                ])
                self.selected_club.club = "Putter"
            case "play-course":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("⛳ Play Course view")
                    ]),
                ])
                self.selected_club.club = "Driver"
        self.selected_club.save_data()
        self.current_section.update()

    def load_home_page(self) -> None:
        self.current_section.content = self.home_page
        self.current_section.update()

    @classmethod
    async def last_shot(cls):
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            return await repo.get_last_shot()

    async def check_db_updates(self) -> None:
        last_data = self.latest_shot_data
        while True:
            await asyncio.sleep(5)
            new_shot_data = await self.last_shot()
            if new_shot_data != last_data:
                logger.info("New shot detected, refreshing section")
                self.latest_shot_data = new_shot_data
                self.drive_range_section = await DriveRangeSection(new_shot_data).build_section()
                if self.current_section_name["name"] == "drive-range":
                    self.update_section("drive-range")
                last_data = new_shot_data


    def update_view(route: str):
        match route:
            case "/drive-range":
                current_view.content = ft.Column([
                    ft.Row([
                        button_return_home,
                        header_selected_section("Drive range")
                    ]),
                    drive_range
                ])
            case "/putting":
                current_view.content = ft.Column([
                    button_return_home,
                    ft.Text("🎯 Putting view", size=30)
                ])
            case "/play-course":
                current_view.content = ft.Column([
                    button_return_home,
                    ft.Text("⛳ Play Course view", size=30)
                ])
        current_view.update()

    home = ft.Container(
        content=ft.Row(
            controls=[
                build_card("/drive-range", "menu/drive-range.png"),
                build_card("/putting", "menu/putting.png"),
                build_card("/play-course", "menu/play-course.png"),
            ],
            expand=True,
            spacing=0
        ),
        expand=True
    )

    current_view.content = home

    return current_view
