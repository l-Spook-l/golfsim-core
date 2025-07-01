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
    headers = (
        "N", "Club", "Ball\n(mph)", "Launch V\n(deg)", "Launch H\n(deg)", "Carry\n(yd)",
        "Roll\n(yd)", "Total\n(yd)", "Lateral\n(yd)", "Spin\n(rpm)", "Date"
    )

    table_header = ft.Row([
        ft.Container(
            content=ft.Text(header, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            width=171,
            bgcolor="#C8E6C9",
            border=ft.border.all(1, "#BDBDBD"),
            border_radius=ft.border_radius.only(top_left=6, top_right=6) if i == 0 else None,
            padding=0,
            margin=0,
            alignment=ft.alignment.center
        )
        for i, header in enumerate(headers)
    ], spacing=0, height=70)

    # Строки таблицы
    table_body = ft.Column(
        controls=[
            ft.Row([
                ft.Container(
                    content=ft.Text(cell, size=16, text_align=ft.TextAlign.CENTER, color="#212121"),
                    width=171,
                    bgcolor="#E8F5E9" if idx % 2 == 0 else "#C8E6C9",  # Зебра
                    border=ft.border.all(1, "#BDBDBD"),
                    # padding=6,
                    alignment=ft.alignment.center,
                )
                for cell in row
            ], spacing=0, height=70)
            for idx, row in enumerate(data)
        ],
        spacing=0,
        height=430,
        scroll=ft.ScrollMode.ALWAYS
    )

    return ft.Container(
        content=ft.Column([
            table_header,
            ft.Divider(
                thickness=3,  # Толщина линии
                color="grey",  # Цвет линии
                height=0
            ),
            table_body
        ], spacing=0
        ),
        border=ft.border.all(1, "#BDBDBD"),
        border_radius=10,
    )
