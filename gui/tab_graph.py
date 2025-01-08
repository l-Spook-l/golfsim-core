import flet as ft
from test_data_club import data_club


golf_hits = data_club["golf_hits"]


class State:
    toggle = True


s = State()


def main(page: ft.Page):
    data_1 = [
        ft.LineChartData(
            # data_points=[
            #     ft.LineChartDataPoint(0, 3),
            #     ft.LineChartDataPoint(2.6, 2),
            #     ft.LineChartDataPoint(4.9, 5),
            #     ft.LineChartDataPoint(6.8, 3.1),
            #     ft.LineChartDataPoint(8, 4),
            #     ft.LineChartDataPoint(9.5, 3),
            #     ft.LineChartDataPoint(11, 4),
            # ],
            data_points=[
                ft.LineChartDataPoint(hit["ball_speed"], hit["distance"]) for hit in golf_hits
            ],
            stroke_width=0,  # Ширина линии диаграммы.
            # color=ft.Colors.CYAN,  # Цвет линии
            # curved=True,   # Установите True для закругления углов (график более плавный). По умолчанию False.
            # stroke_cap_round=True,  # Установите True для рисования закругленных концов линий. По умолчанию False.
            point=True  # True- рисовать точку стилем по умолчанию или False- не рисовать точку линии
        )
    ]

    data_2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3.44),
                ft.LineChartDataPoint(2.6, 3.44),
                ft.LineChartDataPoint(4.9, 3.44),
                ft.LineChartDataPoint(6.8, 3.44),
                ft.LineChartDataPoint(8, 3.44),
                ft.LineChartDataPoint(9.5, 3.44),
                ft.LineChartDataPoint(11, 3.44),
            ],
            stroke_width=5,
            color=ft.Colors.CYAN,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        data_series=data_1,
        border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        # левая строка
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=100,
                    label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=200,
                    label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=250,
                    label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=50,
            title=ft.Text("Carry Distance", size=25),
            title_size=50,

        ),
        # нижняя строка
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "MAR",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Container(
                        ft.Text(
                            "JUN",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=8,
                    label=ft.Container(
                        ft.Text(
                            "SEP",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=50,
            title=ft.Text("Ball Speed", size=25),
            title_size=50,
        ),
        # LineChart - настройки
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=350,
        min_x=0,
        max_x=250,
        animate=500,
        expand=True,
    )

    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.interactive = True
        s.toggle = not s.toggle
        chart.update()

    page.add(ft.ElevatedButton("avg", on_click=toggle_data), chart)


ft.app(main)
