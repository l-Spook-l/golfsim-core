from datetime import datetime

import flet as ft

from states.app_page_state import PageState
from gui.filter_bar import FilterBar
from gui.tab_stat_table import GolfShotTable


class DriveRangeDashboard:
    def __init__(self):
        self.page = PageState.get_page()
        self.load_table = GolfShotTable()
        self.load_filter_bar = FilterBar(dashboard=self)
        self.table = ft.Container()
        self.filter_bar = ft.Container()
        self.view_selector = ft.Tabs()
        self.dashboard_content = ft.Container()
        self.tab_content = ft.Column()

    async def change_view_dashboard(self, e) -> None:
        current_tab = None

        match self.view_selector.selected_index:
            case 0:
                current_tab = self.table
            # TODO: plan to add various charts
            # case 1:
            #     current_tab = self.graph

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
    ) -> None:
        data = await GolfShotTable().load_data(start_date, end_date, club, sort_by, sort_desc, limit_records)
        self.table = await self.load_table.load_stat_table(data)
        self.dashboard_content.content = self.table
        self.dashboard_content.update()

    async def build_section(self) -> ft.Column:
        self.table = await self.load_table.load_stat_table()
        self.filter_bar = await self.load_filter_bar.build_section()

        self.view_selector = ft.Tabs(
            selected_index=0,
            on_change=self.change_view_dashboard,
            tabs=[
                ft.Tab(text="Table"),
            ],
            label_color="black"
        )

        self.dashboard_content = ft.Container(
            content=self.table,
            # margin=ft.margin.all(50),  # Задаем отступы со всех сторон
            # bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),  # Фоновый цвет для визуализации
        )

        self.tab_content = ft.Column(
            [
                self.filter_bar,
                self.view_selector,
                self.dashboard_content
            ],
        )
        return self.tab_content
