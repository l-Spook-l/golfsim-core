import asyncio

import flet as ft

from states.shot_state import ShotState
from ui.components.last_shot_section import LastShotSection
from ui.components.drive_range_dashboard import DriveRangeDashboard
from core.logging_config import logger
from data_base.repositories.golf_shot import GolfShotRepository
from data_base.config_db import async_session_maker


class HomeView:
    """
    Class for managing the main page of the application.

    Main functionality:
    - Forming the main menu (drive range, putting, play course).
    - Loading data about the last shot and displaying the LastShotSection.
    - Switching between sections (update_section).
    - Tracking updates in the database and updating the UI in real-time.

    Attributes:
        home_page (ft.Container): container for the main menu.
        current_section (ft.Container): container for the currently displayed section.
        current_section_name (str): name of the active section.
        latest_shot_data (dict | None): data for the last shot.
        last_shot_section (ft.Container | None): section displaying the last shot.
        button_return_home (ft.IconButton): button to return to the main menu.
        selected_club (ShotState): state of the selected golf club.
        drive_range_dashboard (DriveRangeDashboard | None): dashboard for the driving range.
    """

    def __init__(self):
        self.home_page = ft.Container()
        self.current_section = ft.Container()
        self.current_section_name: str = ""
        self.latest_shot_data = None
        self.last_shot_section = None
        self.button_return_home = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.load_home_page())
        self.selected_club = ShotState()
        self.drive_range_dashboard = None

    async def init(self) -> ft.Container:
        """
        Initializes the main page.

        - Loads data for the last shot.
        - Creates the LastShotSection and DriveRangeDashboard sections.
        - Forms the main menu.

        Returns:
            ft.Container: container for the current section (by default, the main menu).
        """
        self.latest_shot_data = await self.last_shot()
        self.last_shot_section = await LastShotSection(self.latest_shot_data).build_section()
        self.drive_range_dashboard = await DriveRangeDashboard().build_section()

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
        """
        Creates a card for the main menu.

        Args:
            section_name (str): the name of the section (e.g., "drive-range").
            image_url (str): the path to the card image.

        Returns:
            ft.Container: a clickable card.
        """
        return ft.Container(
            content=ft.Image(src=image_url, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
            alignment=ft.alignment.center,
            expand=True,
            margin=10,
            ink=True,
            on_click=lambda e: self.update_section(section_name)
        )

    def update_section(self, section_name: str) -> None:
        """
        Switches the current section based on the selected menu.

        Args:
            section_name (str): the name of the section ("drive-range", "putting", "play-course").
        """
        self.current_section_name = section_name
        match section_name:
            case "drive-range":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("Drive range", size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    self.last_shot_section,
                    self.drive_range_dashboard
                ])
                self.selected_club.club = "Driver"
            case "putting":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("🎯 Putting view")
                    ]),
                    self.last_shot_section
                ])
                self.selected_club.club = "Putter"
            case "play-course":
                self.current_section.content = ft.Column([
                    ft.Row([
                        self.button_return_home,
                        ft.Text("⛳ Play Course view")
                    ]),
                    self.last_shot_section
                ])
                self.selected_club.club = "Driver"
        self.selected_club.save()
        self.current_section.update()

    def load_home_page(self) -> None:
        """
        Returns the user to the main page (main menu).
        """
        self.current_section.content = self.home_page
        self.current_section.update()

    @staticmethod
    async def last_shot():
        """
        Loads the last shot from the database.

        Returns:
            dict | None: the data of the last shot.
        """
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            return await repo.get_last_shot()

    async def check_db_updates(self) -> None:
        """
        Periodically checks the database for new shots.

        - If the data has changed, it updates the "Last Shot" section.
        - If in the "drive-range" section, it updates the dashboard.
        """
        last_data = self.latest_shot_data
        while True:
            await asyncio.sleep(5)
            new_shot_data = await self.last_shot()
            if new_shot_data != last_data:
                logger.info("New shot detected, refreshing section")
                self.latest_shot_data = new_shot_data
                self.last_shot_section = await LastShotSection(new_shot_data).build_section()
                if self.current_section_name == "drive-range":
                    self.drive_range_dashboard = await DriveRangeDashboard().build_section()
                    self.update_section("drive-range")
                last_data = new_shot_data
