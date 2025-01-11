import flet as ft
from datetime import datetime
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
                ft.LineChartDataPoint(
                    hit["ball_speed"], hit["distance"],
                    tooltip=f'{hit["ball_speed"]} and {hit["distance"]}',
                    show_tooltip=True,
                    # selected=True
                    selected_below_line=False
                ) for hit in golf_hits
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

    start_date = ft.TextField(label="Start Date (YYYY-MM-DD)", value="2023-01-01", width=200)
    end_date = ft.TextField(label="End Date (YYYY-MM-DD)", value="2023-12-31", width=200)

    def handle_change_start(e):
        # page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))
        start_date.value = e.control.value.strftime('%Y-%m-%d')
        page.update()

    def handle_change_end(e):
        # page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))
        end_date.value = e.control.value.strftime('%Y-%m-%d')
        page.update()

    # def handle_dismissal(e):
        # page.add(ft.Text(f"DatePicker dismissed"))
        # pass

    select_start_date = ft.ElevatedButton(
        "Start date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=1923, month=1, day=1),
                last_date=datetime.now(),
                on_change=handle_change_start,
                # on_dismiss=handle_dismissal,
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
                # on_dismiss=handle_dismissal,
            )
        ),
    )

    # Функция фильтрации данных
    def filter_data():
        start = datetime.strptime(start_date.value, "%Y-%m-%d")
        end = datetime.strptime(end_date.value, "%Y-%m-%d")

        # Фильтруем данные по дате
        filtered_hits = [
            hit for hit in golf_hits
            if start <= datetime.strptime(hit["date"], "%Y-%m-%d") <= end
        ]

        # Обновляем данные для графика
        chart.data_series = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(hit["ball_speed"], hit["distance"]) for hit in filtered_hits
                ],
                stroke_width=0,
                point=True,
            )
        ]
        chart.update()

    chart = ft.LineChart(
        # interactive=False,
        data_series=data_1,
        border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=50, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=25, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        # левая строка
        left_axis=ft.ChartAxis(
            # labels=[
            #     ft.ChartAxisLabel(
            #         value=100,
            #         label=ft.Text("100", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            #     ft.ChartAxisLabel(
            #         value=200,
            #         label=ft.Text("200", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            #     ft.ChartAxisLabel(
            #         value=300,
            #         label=ft.Text("300", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            # ],
            labels_size=50,
            title=ft.Text("Carry Distance", size=25),
            title_size=50,

        ),
        # нижняя строка
        bottom_axis=ft.ChartAxis(
            # labels=[
            #     ft.ChartAxisLabel(
            #         value=50,
            #         label=ft.Text("50", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            #     ft.ChartAxisLabel(
            #         value=100,
            #         label=ft.Text("100", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            #     ft.ChartAxisLabel(
            #         value=150,
            #         label=ft.Text("150", size=14, weight=ft.FontWeight.BOLD),
            #     ),
            #     # ft.ChartAxisLabel(
            #     #     value=200,
            #     #     label=ft.Text("200", size=14, weight=ft.FontWeight.BOLD),
            #     # ),
            # ],
            labels_size=50,
            labels_interval=25,
            title=ft.Text("Ball Speed", size=25),
            title_size=50,
        ),
        # LineChart - настройки
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=350,
        min_x=0,
        max_x=150,
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

    # page.add(ft.ElevatedButton("avg", on_click=toggle_data), chart)
    # Оборачиваем график в контейнер для отступов
    chart_with_padding = ft.Container(
        content=chart,
        margin=ft.margin.all(50),  # Задаем отступы со всех сторон
        width=800,  # Устанавливаем ширину контейнера
        height=600,  # Устанавливаем высоту контейнера
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),  # Фоновый цвет для визуализации
    )

    # Кнопка обновления данных
    filter_button = ft.ElevatedButton("Filter Data", on_click=lambda _: filter_data())

    # Добавляем график на страницу
    page.add(
        ft.ElevatedButton("avg", on_click=toggle_data),
        ft.Row([start_date, end_date, filter_button, select_start_date, select_end_date],
               alignment=ft.MainAxisAlignment.START),
        chart_with_padding
    )


ft.app(main)
