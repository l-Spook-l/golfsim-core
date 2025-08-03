from datetime import datetime

import flet as ft

from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from data_base.schemas import GolfShotsSchema
from gui.app_context import AppContext


class GolfShotTable:
    def __init__(self):
        self.page = AppContext.get_page()
        self.data_shots = list()
        self.table = ft.Container()

    @staticmethod
    async def load_data(start_date: datetime = None, end_date: datetime = None, club: str = None) -> list:
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            golf_shots = await repo.get_all_shots(start_date, end_date, club)
        return [GolfShotsSchema(**golf_shot.__dict__).as_list() for golf_shot in golf_shots]

    async def load_stat_table(self, data=None) -> ft.Container:
        if not data:
            data = await self.load_data()

        headers = (
            "N", "Club", "Ball\n(mph)", "Launch V\n(deg)", "Launch H\n(deg)", "Carry\n(yd)",
            "Roll\n(yd)", "Total\n(yd)", "Lateral\n(yd)", "Spin\n(rpm)", "Date"
        )

        # Заголовок таблицы
        table_header = ft.Row([
            ft.Container(
                content=ft.Text(header, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                width=171,
                bgcolor="#C8E6C9",
                border=ft.border.all(1, "#BDBDBD"),
                border_radius=ft.border_radius.only(top_left=6, top_right=6) if i == 0 else None,
                padding=0,
                margin=0,
                alignment=ft.alignment.center
            )
            for i, header in enumerate(headers)
        ], spacing=0, height=70)

        # Строки таблицы
        table_body = ft.Column(
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Text(cell, size=16, text_align=ft.TextAlign.CENTER, color="#212121"),
                        width=171,
                        bgcolor="#E8F5E9" if idx % 2 == 0 else "#C8E6C9",  # Зебра
                        border=ft.border.all(1, "#BDBDBD"),
                        alignment=ft.alignment.center,
                    )
                    for cell in row
                ], spacing=0, height=45)
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
                    thickness=3,  # Толщина линии
                    color="grey",  # Цвет линии
                    height=0
                ),
                table_body
            ], spacing=0
            ),
            border=ft.border.all(1, "#BDBDBD"),
            border_radius=10,
        )

        return self.table
