import os
# import json
from datetime import datetime

import flet as ft

from gui.filter_bar import FilterBar
from gui.tab_stat_table import GolfShotTable
# from gui.tab_stat_graph import load_stat_graph
from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from gui.app_context import AppContext

json_path = os.path.join(os.path.dirname(__file__), '../data/clubs.json')

# with open(json_path, 'r', encoding='utf-8') as file:
#     clubs_data = json.load(file)

# unit_system = {
#     "Imperial": {"Distance": "Yards", "Speed": "mph"},
#     "Metric": {"Distance": "Meters", "Speed": "km/h"},
#     "Scientific": {"Distance": "Meters", "Speed": "m/s"},
# }


class DriveRangeDashboard:
    def __init__(self):
        self.page = AppContext.get_page()
        self.load_table = GolfShotTable()
        self.load_filter_bar = FilterBar(dashboard=self)
        self.table = ft.Container()
        self.filter_bar = ft.Container()
        self.view_selector = ft.Tabs()
        self.dashboard_content = ft.Container()
        self.tab_content = ft.Column()

        self.golf_list_clubs = (
            "All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
            "9-Iron", "Pitching Wedge", "Gap Wedge", "Sand wedge", "Lob wedge", "Putter")

        self.chart = ft.Text("Test tab")

    async def change_view_dashboard(self, e):
        current_tab = None

        match self.view_selector.selected_index:
            case 0:
                current_tab = self.table
            case 1:
                current_tab = self.chart

        self.dashboard_content.content = current_tab
        self.dashboard_content.update()
        self.tab_content.update()

    async def update_or_sort_data(
            self,
            start_date: datetime = None,
            end_date: datetime = None,
            club: str = None,
            sort_by: str = None,
            sort_desc: bool = None,
            limit_records: int = None,
    ):
        data = await GolfShotTable().load_data(start_date, end_date, club, sort_by, sort_desc, limit_records)
        self.table = await self.load_table.load_stat_table(data)
        self.dashboard_content.content = self.table
        self.dashboard_content.update()

    async def build_section(self):
        # Загружаем данные
        self.table = await self.load_table.load_stat_table()
        self.filter_bar = await self.load_filter_bar.build_section()

        # панель переключения графиков
        self.view_selector = ft.Tabs(
            selected_index=0,
            on_change=self.change_view_dashboard,
            tabs=[
                ft.Tab(text="Table"),
            ],
            label_color="black"
        )

        # Оборачиваем график в контейнер для отступов
        self.dashboard_content = ft.Container(
            content=self.table,
            # margin=ft.margin.all(50),  # Задаем отступы со всех сторон
            # bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),  # Фоновый цвет для визуализации
        )

        self.tab_content = ft.Column(
            [
                # date_filter_block,
                self.filter_bar,
                self.view_selector,
                # ft.Row([dropdown_select_club, dropdown_select_unit_system], spacing=30),
                self.dashboard_content
            ],
            # scroll=ft.ScrollMode.ALWAYS,
        )

        return self.tab_content
