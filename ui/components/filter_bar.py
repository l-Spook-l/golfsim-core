from datetime import datetime, timedelta

import flet as ft

from states.app_page_state import PageState
from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository


class FilterBar:
    """
    Filter panel component for the golf shot dashboard.

    Provides functionality for:
    - Selecting a date range (quick select and calendar).
    - Filtering by clubs.
    - Sorting by date, ball speed, and carry distance.
    - Limiting the number of records displayed per page.

    Attributes:
        page (PageState): Page object.
        dashboard: Parent dashboard where data is displayed.
        calendar_date_filter_section (ft.Column): Container with date filter widgets.
        start_date (datetime | None): Start date of the filter.
        end_date (datetime | None): End date of the filter.
        dlg_modal (ft.AlertDialog): Date selection dialog.
        label_date (str): Text label for the date range.
        date_range_text (ft.Text): Text displaying the selected date range.
        select_club (str | None): Selected club for filtering.
        sort_by (str): Field to sort by ('date', 'carry', 'ball_speed').
        sort_desc (bool): Sort in descending order if True.
        limit_records (int): Number of records per page.
        golf_list_clubs (tuple[str]): List of available clubs.
    """

    def __init__(self, dashboard):
        self.page = PageState.get_page()
        self.dashboard = dashboard
        self.calendar_date_filter_section = ft.Column()
        self.start_date: datetime | None = None
        self.end_date: datetime | None = None
        self.dlg_modal = ft.AlertDialog()
        self.label_date: str = ""
        self.date_range_text = ft.Text()
        self.select_club: str = ""
        self.sort_by: str = "date"
        self.sort_desc: bool = True
        self.limit_records: int = 10
        self.golf_list_clubs: tuple = (
            "All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
            "9-Iron", "PW", "GW", "SW", "LW", "Putter")

    @staticmethod
    async def fetch_first_shot_date() -> datetime:
        """
        Retrieves the date of the first golf shot record from the database.

        Returns:
            datetime: Date of the first record, or the current date if none exist.
        """
        async with async_session_maker() as session:
            repo = GolfShotRepository(session)
            date = await repo.get_first_shot_date()
            return date if date else datetime.now()

    async def update_table_data(
            self,
            days: int = None,
            club: str = None,
            sort_by: str = None,
            sort_desc: bool = None,
            limit_records: int = None,
    ) -> None:
        """
        Args:
            days (int, optional): Number of recent days to filter by.
            club (str, optional): Selected club.
            sort_by (str, optional): Field to sort by ('date', 'carry', 'ball_speed').
            sort_desc (bool, optional): Sort in descending order.
            limit_records (int, optional): Number of records per page.
        """
        if days is not None:
            self.start_date = (datetime.now() - timedelta(days=days))
        if club is not None:
            if club == "All clubs":
                self.select_club = None
            else:
                self.select_club = club
        if sort_by is not None or sort_desc is not None:
            self.sort_by, self.sort_desc = sort_by, sort_desc
        if limit_records is not None:
            self.limit_records = limit_records

        await self.dashboard.update_or_sort_data(
            self.start_date, self.end_date, self.select_club, self.sort_by, self.sort_desc, self.limit_records
        )
        self.date_range_text.value = f"{self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}"
        self.date_range_text.update()

        if self.calendar_date_filter_section.page is not None:
            self.calendar_date_filter_section.controls[1].controls[1].value = self.start_date.strftime('%Y-%m-%d')
            self.calendar_date_filter_section.controls[2].controls[1].value = self.end_date.strftime('%Y-%m-%d')
            self.calendar_date_filter_section.update()

    def sort_filter(self) -> ft.Dropdown:
        """
        Creates a Dropdown widget for sorting data.

        Returns:
            ft.Dropdown: UI element for selecting sort options.
        """
        async def sort_filter_changed(value):
            match value.data:
                case "ball_speed_desc":
                    await self.update_table_data(sort_by="ball_speed", sort_desc=True)
                case "ball_speed_asc":
                    await self.update_table_data(sort_by="ball_speed", sort_desc=False)
                case "carry_desc":
                    await self.update_table_data(sort_by="carry", sort_desc=True)
                case "carry_asc":
                    await self.update_table_data(sort_by="carry", sort_desc=False)
                case "date_desc":
                    await self.update_table_data(sort_by="date", sort_desc=True)
                case "date_asc":
                    await self.update_table_data(sort_by="date", sort_desc=False)

        sort_filter = ft.Dropdown(
            label="Sort by",
            value="date_desc",
            on_change=sort_filter_changed,
            options=[
                ft.dropdown.Option("date_desc", "Date ↓"),
                ft.dropdown.Option("date_asc", "Date ↑"),
                ft.dropdown.Option("carry_desc", "Carry ↓"),
                ft.dropdown.Option("carry_asc", "Carry ↑"),
                ft.dropdown.Option("ball_speed_desc", "Ball Speed ↓"),
                ft.dropdown.Option("ball_speed_asc", "Ball Speed ↑"),
            ],
            width=160
        )
        return sort_filter

    def select_club_filter(self) -> ft.Dropdown:
        """
        Creates a Dropdown for selecting a club.

        Returns:
            ft.Dropdown: UI element for club selection.
        """
        async def dropdown_changed_club(value):
            await self.update_table_data(club=value.data)

        return ft.Dropdown(
            label="Club",
            value=self.golf_list_clubs[0],
            on_change=dropdown_changed_club,
            options=[
                ft.dropdown.Option(club) for club in self.golf_list_clubs
            ],
            width=185,
            bgcolor="#E8F5E9"
        )

    def update_records_per_page(self) -> ft.Dropdown:
        """
        Creates a Dropdown for selecting the number of records per page.

        Returns:
            ft.Dropdown: UI element for selecting record limit.
        """
        async def dropdown_changed_records_per_page(value):
            await self.update_table_data(limit_records=value.data)

        return ft.Dropdown(
            label="Per page",
            options=[
                ft.dropdown.Option("10"),
                ft.dropdown.Option("20"),
                ft.dropdown.Option("50"),
            ],
            value="10",
            on_change=dropdown_changed_records_per_page
        )

    def quick_date_filter(self) -> ft.Container:
        """
        Creates quick date range selection (7, 30, 90 days and 1 year).

        Returns:
            ft.Container: Container with quick date selection buttons.
        """
        return ft.Container(
            content=ft.Column([
                ft.Text("Quick Select"),
                ft.Column([
                    ft.Row([
                        ft.ElevatedButton("Last 7 Days",
                                          width=100,
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=7)),
                        ft.ElevatedButton("Last 30 Days",
                                          width=100,
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=30)),
                    ]),
                    ft.Row([
                        ft.ElevatedButton("Last 90 Days",
                                          width=100,
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=90)),
                        ft.ElevatedButton("Last Year",
                                          width=100,
                                          on_click=lambda e: self.page.run_task(self.update_table_data, days=360)),
                    ]),
                ]),
            ]),
        )

    def calendar_date_filter(self) -> ft.Column:
        """
        Creates custom date selection with a calendar.

        Returns:
            ft.Column: Container with start and end date selection fields.
        """
        async def handle_change_start(e):
            self.start_date = e.control.value
            await self.update_table_data()

        async def handle_change_end(e):
            self.end_date = e.control.value
            await self.update_table_data()

        self.calendar_date_filter_section = ft.Column([
            ft.Text("Custom Dates"),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="Pick start date",
                    icon_color="#007ACC",
                    on_click=lambda _: self.page.open(
                        ft.DatePicker(
                            first_date=datetime(year=1923, month=1, day=1),
                            last_date=self.end_date,
                            on_change=handle_change_start,
                        )
                    ),
                ),
                ft.TextField(label="Start Date", value=self.start_date.strftime('%Y-%m-%d'), read_only=True, width=150)
            ]),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="Pick end date",
                    icon_color="#007ACC",
                    on_click=lambda _: self.page.open(
                        ft.DatePicker(
                            first_date=self.start_date,
                            last_date=datetime.now(),
                            on_change=handle_change_end,
                        )
                    ),
                ),
                ft.TextField(label="End Date", value=self.end_date.strftime('%Y-%m-%d'), read_only=True, width=150)
            ]),
        ])

        return self.calendar_date_filter_section

    def filter_date_dialog(self, e=None) -> ft.AlertDialog:
        """
        Creates a modal window for selecting a date range.

        Args:
            e (optional): Click event (not used).

        Returns:
            ft.AlertDialog: Date selection dialog.
        """
        return ft.AlertDialog(
            title=ft.Text("Select Date Range"),
            content=ft.Column([
                self.quick_date_filter(),
                ft.Divider(),
                self.calendar_date_filter()
            ], height=270),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(self.dlg_modal))
            ],
        )

    def button_date_filter(self) -> ft.Container:
        """
        Creates a button to open the date selection dialog.

        Returns:
            ft.Container: Button displaying the current date range.
        """
        def on_hover(e):
            e.control.bgcolor = "#A5D6A7" if e.data == "true" else "#E8F5E9"
            e.control.update()

        return ft.Container(
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

    async def build_section(self) -> ft.Container:
        """
        Builds the complete filter block for display on the dashboard.

        Returns:
            ft.Container: Container with the filter button, club selection Dropdown, sorting, and record limit.
        """
        self.start_date = await self.fetch_first_shot_date()
        self.end_date = datetime.now()
        self.dlg_modal = self.filter_date_dialog()
        self.date_range_text = ft.Text(f"{self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}", size=20)

        return ft.Container(
            content=ft.Row(
                [
                    self.button_date_filter(),
                    ft.Row([
                        self.select_club_filter(),
                        self.sort_filter(),
                        self.update_records_per_page()
                    ]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            bgcolor="#C8E6C9",
            border_radius=10,
            height=70,
        )
