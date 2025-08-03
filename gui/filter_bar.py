from datetime import datetime, timedelta

import flet as ft

from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from gui.app_context import AppContext


class FilterBar:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.page = AppContext.get_page()
        self.start_date = ""
        self.end_date = ""
        self.dlg_modal = ft.AlertDialog()
        self.label_date = ""
        self.open_filter_btn = ft.Container()
        self.date_range_text = ft.Text()

    @staticmethod
    async def fetch_first_shot_date() -> datetime:
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            date = await repo.get_first_shot_date()
            return date.strftime('%Y-%m-%d') if date else datetime.now().strftime('%Y-%m-%d')

    async def update_table_data(self, days: int = None):
        if days:
            self.start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        await self.dashboard.update(self.start_date, self.end_date)
        self.date_range_text.value = f"{self.start_date} - {self.end_date}"
        self.date_range_text.update()

    def quick_date_sort(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Text("Quick Select"),
                ft.Column([
                    ft.Row([
                        ft.ElevatedButton("Last 7 Days",
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=7)),
                        ft.ElevatedButton("Last 30 Days",
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=30)),
                    ]),
                    ft.Row([
                        ft.ElevatedButton("Last 90 Days",
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=90)),
                        ft.ElevatedButton("Last Year",
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=360)),
                    ]),
                ]),
            ]),
        )

    def calendar_date_filter(self):
        def handle_change_start(e):
            self.start_date = e.control.value.strftime('%Y-%m-%d')
            self.page.run_task(self.update_table_data)

        def handle_change_end(e):
            self.end_date = e.control.value.strftime('%Y-%m-%d')
            self.page.run_task(self.update_table_data)

        return ft.Column([
            ft.Text("Custom Dates"),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    # tooltip="Pick start date",
                    # icon_color="#007ACC",
                    on_click=lambda _: self.page.open(
                        ft.DatePicker(
                            first_date=datetime(year=1923, month=1, day=1),
                            last_date=datetime.now(),
                            on_change=handle_change_start,
                        )
                    ),
                    # style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=ft.padding.all(6))
                ),
                ft.TextField(label="Start Date", value=self.start_date, read_only=True, width=150)
            ]),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    # tooltip="Pick end date",
                    # icon_color="#007ACC",
                    on_click=lambda _: self.page.open(
                        ft.DatePicker(
                            first_date=datetime(year=1923, month=1, day=1),
                            last_date=datetime.now(),
                            on_change=handle_change_end,
                        )
                    ),
                    # style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=ft.padding.all(6))
                ),
                ft.TextField(label="End Date", value=self.end_date, read_only=True, width=150)
            ]),
        ])

    def show_filter_dialog(self, e=None):
        return ft.AlertDialog(
            title=ft.Text("Select Date Range"),
            content=ft.Column([
                self.quick_date_sort(),
                ft.Divider(),
                self.calendar_date_filter()
            ], height=280),
            actions=[
                ft.TextButton("Apply", on_click=lambda e: self.page.close(self.dlg_modal)),
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(self.dlg_modal))
            ],
        )

    async def build_section(self):
        self.start_date = await self.fetch_first_shot_date()
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.dlg_modal = self.show_filter_dialog()
        self.date_range_text = ft.Text(f"{self.start_date} - {self.end_date}", size=20)

        def on_hover(e):
            e.control.bgcolor = "#A5D6A7" if e.data == "true" else "#E8F5E9"
            e.control.update()

        self.open_filter_btn = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.Icons.CALENDAR_MONTH),
                self.date_range_text,
            ]),
            padding=5,
            bgcolor="#E8F5E9",
            border=ft.border.all(1, "#BDBDBD"),
            border_radius=7,
            on_hover=on_hover,
            on_click=lambda e: self.page.open(self.dlg_modal),
        )

        return ft.Container(
            content=ft.Row([self.open_filter_btn]),
            padding=10,
            bgcolor="#C8E6C9",
            border_radius=10,
            height=70,
        )
