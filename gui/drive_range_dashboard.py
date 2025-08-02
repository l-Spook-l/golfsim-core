import os
# import json
from datetime import datetime

import flet as ft

from gui.tab_stat_table import load_stat_tab
# from gui.tab_stat_graph import load_stat_graph
from data_base.config_db import async_session_maker
from data_base.repositories.golf_shot import GolfShotRepository
from gui.app_context import AppContext

json_path = os.path.join(os.path.dirname(__file__), '../data/clubs.json')

# with open(json_path, 'r', encoding='utf-8') as file:
#     clubs_data = json.load(file)

golf_list_clubs = ("All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
                   "9-Iron", "Pitching Wedge", "Gap Wedge", "Sand wedge", "Lob wedge", "Putter")


# unit_system = {
#     "Imperial": {"Distance": "Yards", "Speed": "mph"},
#     "Metric": {"Distance": "Meters", "Speed": "km/h"},
#     "Scientific": {"Distance": "Meters", "Speed": "m/s"},
# }


class DriveRangeDashboard:
    def __init__(self):
        self.page = AppContext.get_page()
        self.table = ft.Container()
        self.tabs = ft.Tabs()
        self.dashboard_content = ft.Column()

    async def change_view_graph(self, e):
        # nonlocal date_filter_block  # Позволяет менять переменную в родительской области

        # Определяем текущий активный контент (график или таблица)
        current_tab = None

        match self.tabs.selected_index:
            case 0:
                current_tab = self.table
            # case 1:
            #     current_tab = chart

        # chart_with_padding.content = current_tab  # Меняем контент

        # Пересоздаем фильтр, передавая текущий активный элемент
        # date_filter_block.content = await create_filter_bar(
        #     # current_tab, tabs.selected_index, page, dropdown_select_club, dropdown_select_unit_system
        #     current_tab, tabs.selected_index, page, dropdown_select_club, dropdown_sort
        # )

        # date_filter_block.update()
        self.dashboard_content.update()

    async def build_section(self):
        # Загружаем данные
        self.table = await load_stat_tab()

        # chart = await load_stat_graph()
        chart = ft.Text("sadddddddddddd")

        tabs = ft.Tabs(
            selected_index=0,
            on_change=self.change_view_graph,
            tabs=[
                ft.Tab(text="Table"),
                # ft.Tab(text="Graph"),  # график временно убран
            ],
            label_color="black"
        )

        # async def change_view(e):
        #     # nonlocal chart
        #     if s.toggle:
        #         chart_with_padding.content = load_stat_graph(page)  # LineChart
        #         # chart = load_stat_graph(page)  # LineChart
        #
        #         # chart.interactive = True
        #     else:
        #         chart_with_padding.content = await load_stat_tab()  # DataTable
        #         # chart = load_stat_tab()  # DataTable
        #
        #         # chart.interactive = False
        #     # page.add(chart)
        #
        #     s.toggle = not s.toggle
        #     chart_with_padding.update()
        #     # chart = chart_with_padding
        #
        #     # chart.update()
        #     # page.update()

        # Оборачиваем график в контейнер для отступов
        chart_with_padding = ft.Container(
            content=self.table,
            # margin=ft.margin.all(50),  # Задаем отступы со всех сторон
            # bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),  # Фоновый цвет для визуализации
        )

        # # Создаем элементы UI
        # # dropdown_select_club, dropdown_select_unit_system = create_dropdowns(chart, page)
        # dropdown_select_club, dropdown_sort = create_dropdown(chart, page)
        #
        # date_filter_block = await create_filter_bar(
        #     # table, tabs.selected_index, page, dropdown_select_club, dropdown_select_unit_system
        #     table, tabs.selected_index, page, dropdown_select_club, dropdown_sort
        # )

        dashboard_content = ft.Column(
            [
                # date_filter_block,
                tabs,
                # ft.Row([dropdown_select_club, dropdown_select_unit_system], spacing=30),
                chart_with_padding
            ],
            # scroll=ft.ScrollMode.ALWAYS,
        )

        return dashboard_content
