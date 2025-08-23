import flet as ft

from data_base.config_db import async_session_maker
# from data_base.db import DataBase
# from ui.components.general_settings import unit_system

# golf_list_clubs = ("All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
#                    "9-Iron", "Pitching Wedge", "Gap Wedge", "Sand wedge", "Lob wedge", "Putter")


async def load_data() -> list:
    async with async_session_maker() as session:  # Создание сессии
        golf_shots = await DataBase.get_data(session=session)  # Передача сессии в метод
        # print("load_data() - data - ", golf_shots[0])

    return golf_shots


async def load_stat_graph(page: ft.Page = None):
    data = await load_data()

    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(
                    hit.ball_speed, hit.carry,
                    tooltip=f'{hit.ball_speed} and {hit.carry}',
                    show_tooltip=True,
                    # selected=True
                    selected_below_line=False
                ) for hit in data
            ],
            stroke_width=0,  # Ширина линии диаграммы.
            # color=ft.Colors.CYAN,  # Цвет линии
            # curved=True,   # Установите True для закругления углов (график более плавный). По умолчанию False.
            # stroke_cap_round=True,  # Установите True для рисования закругленных концов линий. По умолчанию False.
            point=True  # True- рисовать точку стилем по умолчанию или False- не рисовать точку линии
        )
    ]

    graph = ft.LineChart(
        # interactive=False,
        data_series=data_1,
        border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=50, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=25, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        top_axis=ft.ChartAxis(
            title=ft.Text(f"{'Club - All clubs'}", size=25),
            title_size=50,
            show_labels=False,
        ),
        # левая строка
        left_axis=ft.ChartAxis(
            labels_size=50,
            title=ft.Text(f"Carry Distance ({unit_system.get('Imperial').get('Distance')})", size=25),
            title_size=50,

        ),
        # нижняя строка
        bottom_axis=ft.ChartAxis(
            labels_size=30,
            labels_interval=25,
            title=ft.Text(f"Carry Distance ({unit_system.get('Imperial').get('Speed')})", size=25),
            title_size=50,
        ),
        # right_axis=ft.ChartAxis(labels=None, labels_size=100),

        # LineChart - настройки
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=350,
        min_x=0,
        max_x=150,
        # animate=500,
        # expand=True,
        width=800
    )

    tab_content = graph

    return tab_content

