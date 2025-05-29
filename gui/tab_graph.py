import os
import json
from datetime import datetime

import flet as ft

from .tab_stat_table import load_stat_tab
from .tab_stat_graph import load_stat_graph
from data_base.config_db import async_session_maker
from data_base.db import DataBase

json_path = os.path.join(os.path.dirname(__file__), '../data/clubs.json')
with open(json_path, 'r', encoding='utf-8') as file:
    clubs_data = json.load(file)

golf_list_clubs = ("All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
                   "9-Iron", "Pitching Wedge", "Gap Wedge", "Sand wedge", "Lob wedge", "Putter")

unit_system = {
    "Imperial": {"Distance": "Yards", "Speed": "mph"},
    "Metric": {"Distance": "Meters", "Speed": "km/h"},
    "Scientific": {"Distance": "Meters", "Speed": "m/s"},
}


async def get_first_shot_date():
    async with async_session_maker() as session:
        first_shot = await DataBase.get_first_shot(session)
        return first_shot.date if first_shot else datetime.now()


def create_dropdown(chart, page):
    def dropdown_changed_club(value):
        page.defer_update = True  # Отключаем авто обновление временно
        chart.top_axis = ft.ChartAxis(
            title=ft.Text(f"Club - {value.data}", size=25),
            title_size=50,
            show_labels=False)
        chart.update()

    # def dropdown_changed_unit_system(value):
    #     # t.value = f"Dropdown changed to {dropdown_select_unit_system.value}"
    #
    #     chart.left_axis = ft.ChartAxis(
    #         labels_size=50,
    #         title=ft.Text(
    #             f"Carry Distance ({unit_system.get(value.data).get('Distance')})", size=25),
    #         title_size=50,
    #     )
    #
    #     chart.bottom_axis = ft.ChartAxis(
    #         labels_size=30,
    #         labels_interval=25,
    #         title=ft.Text(
    #             f"Ball Speed ({unit_system.get(value.data).get('Speed')})", size=25),
    #         title_size=50,
    #     )
    #     chart.update()

    dropdown_select_club = ft.Dropdown(
        value=golf_list_clubs[0],  # Значение по умолчанию
        on_change=dropdown_changed_club,
        options=[
            ft.dropdown.Option(club) for club in golf_list_clubs
        ],
        width=200,
    )

    dropdown_sort = ft.Dropdown(
        label="Sort by",
        value="ball_speed_desc",  # значение по умолчанию
        options=[
            ft.dropdown.Option("date_desc", "Date ↓"),
            ft.dropdown.Option("date_asc", "Date ↑"),
            ft.dropdown.Option("carry_desc", "Carry ↓"),
            ft.dropdown.Option("carry_asc", "Carry ↑"),
            ft.dropdown.Option("ball_speed_desc", "Ball Speed ↓"),
            ft.dropdown.Option("ball_speed_asc", "Ball Speed ↑"),
        ],
        width=120
    )

    # dropdown_select_unit_system = ft.Dropdown(
    #     value="Imperial",
    #     on_change=dropdown_changed_unit_system,
    #     options=[
    #         ft.dropdown.Option(system) for system in unit_system.keys()
    #     ],
    #     width=150,
    # )

    # return dropdown_select_club, dropdown_select_unit_system
    return dropdown_select_club


def update_chart_data(chart, data):
    chart.data_series = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(hit.ball_speed, hit.carry) for hit in data
            ],
            stroke_width=0,
            point=True,
        )
    ]
    chart.update()


def update_table_data(table, data):
    res = [
        [
            str(golf_shot.id),
            str(golf_shot.ball_speed),
            str(golf_shot.angle_v),
            str(golf_shot.angle_h),
            str(golf_shot.carry),
            str(golf_shot.roll),
            str(golf_shot.total),
            str(golf_shot.lateral),
            str(golf_shot.spin),
            golf_shot.date.strftime("%d-%m-%Y %H:%M:%S"),
        ]
        for golf_shot in data
    ]

    table.rows = [
        ft.DataRow(
            cells=[ft.DataCell(ft.Text(cell, size=18, text_align=ft.TextAlign.CENTER, width=95)) for cell in row])
        for row in res
    ]

    table.update()


# Функция фильтрации данных
async def create_filter_bar(tab, index_tab: int, page, dropdown_select_club, dropdown_sort):
    first_date = await get_first_shot_date()
    first_str = first_date.strftime('%Y-%m-%d')
    now_str = datetime.now().strftime('%Y-%m-%d')

    start_date = ft.TextField(
        label="Start Date",
        value=first_str,
        width=150,
        text_size=16,
        read_only=True
    )

    end_date = ft.TextField(
        label="End Date",
        value=now_str,
        width=150,
        text_size=16,
        read_only=True
    )

    def handle_change_start(e):
        start_date.value = e.control.value.strftime('%Y-%m-%d')
        start_date.update()

    def handle_change_end(e):
        end_date.value = e.control.value.strftime('%Y-%m-%d')
        end_date.update()

    select_start_date = ft.ElevatedButton(
        "Start date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=1923, month=1, day=1),
                last_date=datetime.now(),
                on_change=handle_change_start,
            )
        ),
    )

    select_end_date = ft.ElevatedButton(
        "End date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=1923, month=1, day=1),
                last_date=datetime.now(),
                on_change=handle_change_end,
            )
        ),
    )

    async def filter_data():
        start = datetime.strptime(start_date.value, "%Y-%m-%d")
        end = datetime.strptime(end_date.value, "%Y-%m-%d")

        async with async_session_maker() as session:
            filtered_shots = await DataBase.get_data(session, start, end)

        print('filter_data filtered_shots', filtered_shots)
        match index_tab:
            case 0:
                update_table_data(tab, filtered_shots)
            case 1:
                update_chart_data(tab, filtered_shots)

    async def handle_click(_):
        await filter_data()

    # Кнопка обновления данных
    filter_button = ft.ElevatedButton("Filter Data", on_click=handle_click)

    return ft.Container(
        content=ft.Row(
            [
                filter_button,
                select_start_date,
                start_date,
                select_end_date,
                end_date,
                # ft.Column([ft.Text("Select club", size=22), dropdown_select_club]),
                # ft.Text("Select club", size=22),
                dropdown_select_club
                # ft.Column([ft.Text("Select unit system", size=22), dropdown_select_unit_system]),
            ],
            spacing=30,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
        # height=100,
    )


async def load_stat(page: ft.Page):
    # Загружаем данные
    table = await load_stat_tab()
    chart = await load_stat_graph()

    async def change_view_graph(e):
        nonlocal date_filter_block  # Позволяет менять переменную в родительской области

        # Определяем текущий активный контент (график или таблица)
        current_tab = None

        match tabs.selected_index:
            case 0:
                current_tab = table
            case 1:
                current_tab = chart

        chart_with_padding.content = current_tab  # Меняем контент

        # Пересоздаем фильтр, передавая текущий активный элемент
        date_filter_block.content = await create_filter_bar(
            # current_tab, tabs.selected_index, page, dropdown_select_club, dropdown_select_unit_system
            current_tab, tabs.selected_index, page, dropdown_select_club
        )

        date_filter_block.update()
        tab_content.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=change_view_graph,
        tabs=[
            ft.Tab(text="Table"),
            ft.Tab(text="Graph"),
        ],
        # expand=1,
    )


    # Оборачиваем график в контейнер для отступов
    chart_with_padding = ft.Container(
        content=table,
        # margin=ft.margin.all(50),  # Задаем отступы со всех сторон
        # width=1100,  # Устанавливаем ширину контейнера
        # height=550,  # Устанавливаем высоту контейнера
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),  # Фоновый цвет для визуализации
    )

    # Создаем элементы UI
    # dropdown_select_club, dropdown_select_unit_system = create_dropdowns(chart, page)
    dropdown_select_club = create_dropdown(chart, page)

    date_filter_block = await create_filter_bar(
        # table, tabs.selected_index, page, dropdown_select_club, dropdown_select_unit_system
        table, tabs.selected_index, page, dropdown_select_club
    )

    tab_content = ft.Column(
        [
            date_filter_block,
            tabs,
            # ft.Row([dropdown_select_club, dropdown_select_unit_system], spacing=30),
            chart_with_padding
        ],
        # scroll=ft.ScrollMode.ALWAYS,
    )

    return tab_content
