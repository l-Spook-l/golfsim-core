import flet as ft
from .tab_graph import load_stat

from data_base.db import DataBase
from data_base.config_db import async_session_maker

last_hit_title = ("Carry (yd)", "Ball (mph)", "Launch V ", "Launch H ")


async def last_shot():
    async with async_session_maker() as session:  # Создание сессии
        shot = await DataBase.get_last_shot(session=session)  # Передача сессии в метод
    print('last shot', shot)
    print('last shot', type(shot))
    return shot


async def load_home(page: ft.Page):
    page.title = "Data Panel"
    page.padding = 20

    last_hit = await last_shot()

    carry, ball_speed, angle_v, angle_h = last_hit

    print('last_hit', last_hit)
    print('carry, ball_speed, angle_v, angle_h', carry, ball_speed, angle_v, angle_h)

    # Заголовок панели
    data_panel_title = ft.Container(
        content=ft.Text("Drive range", size=28, weight=ft.FontWeight.BOLD),
        border=ft.border.all(2),
    )

    last_hit_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(header, size=28, text_align=ft.TextAlign.CENTER, width=150)) for header in
                 last_hit_title],

        rows=[ft.DataRow(
            cells=[ft.DataCell(ft.Text(cell, size=25, text_align=ft.TextAlign.CENTER, width=150, bgcolor="green"))
                   for
                   cell in last_hit], color="yellow")
        ],
        bgcolor="blue",
        border=ft.border.all(2, "red"),
        border_radius=10,
        vertical_lines=ft.BorderSide(3, "black"),
        horizontal_lines=ft.BorderSide(1, "green"),
        width=850,
        # height=500
        # column_spacing=20,  # Отступы между колонками
        # data_row_min_height=40,  # Минимальная высота строки
    )

    home = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    data_panel_title,
                    last_hit_table
                ]),
                bgcolor=ft.Colors.BLUE
            ),
            ft.Container(
                content=await load_stat(page),
                bgcolor=ft.Colors.ORANGE_100
            ),
        ]),
        bgcolor=ft.Colors.CYAN_100
    )

    return home
