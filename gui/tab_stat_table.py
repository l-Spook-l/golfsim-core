import flet as ft

from data_base.config_db import async_session_maker
from data_base.db import DataBase


async def load_data() -> list:
    async with async_session_maker() as session:  # Создание сессии
        golf_shots = await DataBase.get_data(session=session)  # Передача сессии в метод
        print("data - ", golf_shots[0])
        data = [
            [
                str(golf_shot.id),
                str(golf_shot.club),
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
            for golf_shot in golf_shots
        ]

    return data


async def load_stat_tab():
    # page.scroll = "adaptive"

    # Заголовки столбцов
    headers = (
        "N", "Club", "Ball\n(mph)", "Launch V\n(deg)", "Launch H\n(deg)", "Carry\n(yd)", "Roll\n(yd)", "Total\n(yd)",
        "Lateral\n(yd)", "Spin\n(rpm)", "Date"
    )

    data = await load_data()

    # Создание таблицы

    table_header = ft.Row([
        ft.Container(
            content=ft.Text(header, size=19, text_align=ft.TextAlign.CENTER),
            # alignment=ft.alignment.center,
            width=95,
            bgcolor="orange"
        )
        for header in headers
    ])

    table_body = ft.Column([
        ft.Row(
            [
                ft.Container(
                    content=ft.Text(cell, size=18, text_align=ft.TextAlign.CENTER),
                    # alignment=ft.alignment.center,
                    width=95
                )
                for cell in row
            ]
        )
        for row in data
    ])

    return ft.Container(
        content=ft.Column([
            table_header,
            ft.Column(
                controls=[table_body],
                height=450,
                scroll=ft.ScrollMode.ALWAYS  # заставляет колонку прокручиваться
            )
        ]),
        border=ft.border.all(1, "grey"),
        border_radius=10,
    )
