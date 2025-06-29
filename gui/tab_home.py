import asyncio

import flet as ft

from gui.drive_range_section import load_drive_range_section
from logging_config import logger
from data_base.db import DataBase
from data_base.config_db import async_session_maker


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.home = ft.Container()
        self.current_section = ft.Container()
        self.current_section_name = {"name": ""}
        self.latest_shot_data = None
        self.drive_range = None
        self.button_return_home = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.show_home())

    async def init(self) -> ft.Container:
        # self.latest_shot_data = await DataBase.get_last_shot(session=async_session_maker())
        self.latest_shot_data = await self.last_shot()
        self.drive_range = await load_drive_range_section(self.page, self.latest_shot_data)

        self.home = ft.Container(
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

        self.current_section.content = self.home
        asyncio.ensure_future(self.check_db_updates())
        return self.current_section

    def build_card(self, section_name, image_url):
        return ft.Container(
            content=ft.Image(src=image_url, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
            alignment=ft.alignment.center,
            expand=True,
            margin=10,
            ink=True,
            on_click=lambda e: self.update_section(section_name)
        )

    def update_section(self, section: str):
        self.current_section_name["name"] = section
        match section:
            case "drive-range":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("Drive range", size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    self.drive_range
                ])
            case "putting":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("🎯 Putting view")
                    ]),
                ])
            case "play-course":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("⛳ Play Course view")
                    ]),
                ])
        self.current_section.update()

    def show_home(self):
        self.current_section.content = self.home
        self.current_section.update()

    @classmethod
    async def last_shot(cls):
        """Returns data about the last shot (from the database)"""
        async with async_session_maker() as session:
            return await DataBase.get_last_shot(session=session)

    async def check_db_updates(self):
        last_data = self.latest_shot_data
        while True:
            await asyncio.sleep(5)
            async with async_session_maker() as session:
                new_data = await DataBase.get_last_shot(session=session)
                if new_data != last_data:
                    logger.info("New shot detected, refreshing section")
                    self.latest_shot_data = new_data
                    self.drive_range = await load_drive_range_section(self.page, new_data)
                    if self.current_section_name["name"] == "drive-range":
                        self.update_section("drive-range")
                    last_data = new_data

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
