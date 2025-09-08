from datetime import datetime

import flet as ft

from states.app_page_state import PageState
from ui.components.filter_bar import FilterBar
from ui.components.tab_stat_table import GolfShotTable


class DriveRangeDashboard:
    """
    Main dashboard section for displaying golf shot statistics in tabular form.

    Handles:
    - Filter bar interactions
    - Tab switching (e.g., table, future charts)
    - Data loading and sorting
    """

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
        """
        Handles tab switching in the dashboard.
        Currently only supports switching to the table tab.

        Args:
            e (ft.ControlEvent): Event from tab change.
        """
        current_tab = None

        match self.view_selector.selected_index:
            case 0:
                current_tab = self.table
            # case 1: Future charts or graphs could be added here.

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
        """
        Updates table content with filtered or sorted data.

        Args:
            start_date (datetime, optional): Filter by start date.
            end_date (datetime, optional): Filter by end date.
            club (str, optional): Filter by club name.
            sort_by (str, optional): Column name to sort by.
            sort_desc (bool, optional): Sort descending if True.
            limit_records (int, optional): Limit number of records.
        """
        data = await GolfShotTable().load_data(start_date, end_date, club, sort_by, sort_desc, limit_records)
        self.table = await self.load_table.load_stat_table(data)
        self.dashboard_content.content = self.table
        self.dashboard_content.update()

    async def build_section(self) -> ft.Column:
        """
        Builds the entire dashboard UI section including the table, filters, and tabs.

        Returns:
            ft.Column: Flet Column widget containing all dashboard components.
        """
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
        )

        self.tab_content = ft.Column(
            [
                self.filter_bar,
                self.view_selector,
                self.dashboard_content
            ],
        )
        return self.tab_content
