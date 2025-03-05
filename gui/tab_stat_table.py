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
        "N", "Ball (mph)", "Launch V (deg)", "Launch H (deg)", "Carry (yd)", "Roll (yd)", "Total (yd)", "Lateral (yd)",
        "Spin (rpm)", "Date"
    )

    data = await load_data()

    # Создание таблицы
    table = ft.DataTable(
        # width=700,
        # height=500,
        bgcolor="yellow",
        border=ft.border.all(2, "red"),
        border_radius=10,
        columns=[ft.DataColumn(ft.Text(header, size=19, text_align=ft.TextAlign.CENTER, width=95)) for header in
                 headers],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(cell, size=18, text_align=ft.TextAlign.CENTER, width=95)) for cell in row])
            for row in data
        ]
    )

    return table
