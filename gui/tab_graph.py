import flet as ft
from datetime import datetime
from test_data_club import data_club


golf_list_clubs = ("All clubs", "Driver", "3-Wood", "5-Wood", "4-Iron", "5-Iron", "6-Iron", "7-Iron", "8-Iron",
                   "9-Iron", "Pitching Wedge", "Gap Wedge", "Sand wedge", "Lob wedge", "Putter")

unit_system = {
    "Imperial": {"Distance": "Yards", "Speed": "mph"},
    "Metric": {"Distance": "Meters", "Speed": "km/h"},
    "Scientific": {"Distance": "Meters", "Speed": "m/s"},
}


def create_dropdowns(chart, page):
    def dropdown_changed_club(value):
        page.defer_update = True  # Отключаем авто обновление временно
        chart.top_axis = ft.ChartAxis(
            title=ft.Text(f"Club - {value.data}", size=25),
            title_size=50,
            show_labels=False)
        chart.update()

    def dropdown_changed_unit_system(value):
        chart.left_axis = ft.ChartAxis(
            labels_size=50,
            title=ft.Text(
                f"Carry Distance ({unit_system.get(value.data).get('Distance')})", size=25),
            title_size=50,
        )

        chart.bottom_axis = ft.ChartAxis(
            labels_size=30,
            labels_interval=25,
            title=ft.Text(
                f"Ball Speed ({unit_system.get(value.data).get('Speed')})", size=25),
            title_size=50,
        )
        chart.update()

    dropdown_select_club = ft.Dropdown(
        value=golf_list_clubs[0],  # Значение по умолчанию
        on_change=dropdown_changed_club,
        options=[
            ft.dropdown.Option(club) for club in golf_list_clubs
        ],
        width=150,
    )

    dropdown_select_unit_system = ft.Dropdown(
        value="Imperial",
        on_change=dropdown_changed_unit_system,
        options=[
            ft.dropdown.Option(system) for system in unit_system.keys()
        ],
        width=150,
    )

    return dropdown_select_club, dropdown_select_unit_system


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
async def create_date_filter(tab, index_tab: int, page, dropdown_select_club, dropdown_select_unit_system):
    start_date = ft.TextField(label="Start Date (YYYY-MM-DD)", value=datetime.now().strftime('%Y-%m-%d'), width=180,
                              text_size=18, read_only=True)
    end_date = ft.TextField(label="End Date (YYYY-MM-DD)", value=datetime.now().strftime('%Y-%m-%d'), width=180,
                            text_size=18, read_only=True)

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

        print('filter_data - filtered_shots', filtered_shots)
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
                ft.Column(
                    [ft.Row([select_start_date, select_end_date]),
                     ft.Row([start_date, end_date]), ]
                ),
                ft.Column([ft.Text("Select club", size=22), dropdown_select_club]),
                ft.Column([ft.Text("Select unit system", size=22), dropdown_select_unit_system]),
            ],
            spacing=30,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
        # height=100,
    )

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
            title=ft.Text(f"Carry Distance ({unit_system.get('Imperial').get('Speed')})", size=25),
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

    select_date_block = ft.Container(
        # content=ft.Row([start_date, end_date, filter_button, select_start_date, select_end_date],
        #                alignment=ft.MainAxisAlignment.START),
        content=ft.Column(
            [
                ft.Row([filter_button, select_start_date, select_end_date]),
                ft.Row([start_date, end_date]),
                ft.Row([ft.Text("Select club", size=22), dropdown_select_club]),
                ft.Row([ft.Text("Select unit system", size=22), dropdown_select_unit_system]),
            ],
            spacing=30,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
    )

    # Добавляем график на страницу
    page.add(
        ft.ElevatedButton("avg", on_click=toggle_data),
        # ft.Row([start_date, end_date, filter_button, select_start_date, select_end_date],
        #        alignment=ft.MainAxisAlignment.START),
        ft.Row([chart_with_padding, select_date_block])
        # select_date_block,
        # chart_with_padding,
    )


ft.app(main)
