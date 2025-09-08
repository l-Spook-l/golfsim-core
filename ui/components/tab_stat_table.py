from datetime import datetime

import flet as ft

from states.app_page_state import PageState
from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from data_base.schemas import GolfShotsSchema


class GolfShotTable:
    """
    Class for displaying golf shot statistics as a table.

    Main functionality:
    - Loading shot data from the database
    - Creating a table with results (headers and rows)
    - Sorting and filtering data by date, club, and other parameters

    Attributes:
        page (PageState): the current page object in Flet
        table (ft.Container): a container for the table to display in the UI
    """

    def __init__(self):
        self.page = PageState.get_page()
        self.table = ft.Container()

    @staticmethod
    async def load_data(
            start_date: datetime = None,
            end_date: datetime = None,
            club: str = None,
            sort_by: str = "date",
            sort_desc: bool = True,
            limit_records: int = 10
    ) -> list:
        """
        Loads shot data from the database with filtering and sorting.

        Args:
            start_date (datetime, optional): the start date for the selection.
            end_date (datetime, optional): the end date for the selection.
            club (str, optional): the name of the club for filtering.
            sort_by (str): the field to sort by (default is "date").
            sort_desc (bool): whether to sort in descending order (default is True).
            limit_records (int): the maximum number of records (default is 10).

        Returns:
            list: a list of shots in the format `GolfShotsSchema.as_list()`.
        """
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            golf_shots = await repo.get_all_shots(start_date, end_date, club, sort_by, sort_desc, limit_records)
        return [GolfShotsSchema(**golf_shot.__dict__).as_list() for golf_shot in golf_shots]

    async def load_stat_table(self, data=None) -> ft.Container:
        """
        Generates a UI table for golf shot statistics.

        Args:
            data (list | None): the data to be displayed.
                If None, data is loaded through `load_data`.

        Returns:
            ft.Container: a container with the table (header + rows).
        """
        if data is None:
            data = await self.load_data()

        headers = (
            "N", "Club", "Ball\n(mph)", "Launch V\n(deg)", "Launch H\n(deg)", "Carry\n(yd)",
            "Roll\n(yd)", "Total\n(yd)", "Lateral\n(yd)", "Spin\n(rpm)", "Date"
        )

        # Table header
        table_header = ft.Row([
            ft.Container(
                content=ft.Text(header, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                width=174,
                bgcolor="#C8E6C9",
                border=ft.border.all(1, "#BDBDBD"),
                border_radius=ft.border_radius.only(top_left=6, top_right=6) if i == 0 else None,
                padding=0,
                margin=0,
                alignment=ft.alignment.center
            )
            for i, header in enumerate(headers)
        ], spacing=0, height=70)

        # Table rows
        table_body = ft.Column(
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Text(cell, size=16, text_align=ft.TextAlign.CENTER, color="#212121"),
                        width=174,
                        bgcolor="#E8F5E9" if idx % 2 == 0 else "#C8E6C9",
                        border=ft.border.all(1, "#BDBDBD"),
                        alignment=ft.alignment.center,
                    )
                    for cell in row
                ], spacing=0, height=48)
                for idx, row in enumerate(data)
            ],
            spacing=0,
            height=485,
            scroll=ft.ScrollMode.ALWAYS
        )

        self.table = ft.Container(
            content=ft.Column([
                table_header,
                ft.Divider(
                    thickness=3,
                    color="grey",
                    height=0
                ),
                table_body
            ], spacing=0
            ),
            border=ft.border.all(1, "#BDBDBD"),
            border_radius=10,
        )

        return self.table
