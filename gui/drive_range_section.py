import os
import json

import flet as ft

from gui.tab_graph import load_stat
from data_base.db import DataBase
from data_base.config_db import async_session_maker
from logging_config import logger

last_hit_title = ("Carry (yd)", "Ball (mph)", "Launch V ", "Launch H ")


async def clubs_info() -> dict:
    data = {}  # значение по умолчанию

    if os.path.exists("data/clubs.json"):
        with open("data/clubs.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)['clubs']
            except json.JSONDecodeError:
                logger.info("⚠️ Файл повреждён. Создаём заново.")

    logger.info(f'path - {os.path.exists("settings.json")}')
    logger.info(f'data - {data}')

    return data


async def last_shot():
    async with async_session_maker() as session:  # Создание сессии
        shot = await DataBase.get_last_shot(session=session)  # Передача сессии в метод
    logger.info(f'last shot {shot}, type - {type(shot)}')
    return shot


async def load_drive_range_section(page: ft.Page):
    page.padding = 20

    last_hit = await last_shot()

    carry, ball_speed, angle_v, angle_h = last_hit

    golf_clubs = await clubs_info()
    active_club = {
        "name": golf_clubs[0]["name"],
        "image": golf_clubs[0]["image"]
    }

    logger.info(f'last_hit, {last_hit}')
    logger.info(f'carry, ball_speed, angle_v, angle_h, {carry}, {ball_speed}, {angle_v}, {angle_h}')

    # Заголовок панели
    data_panel_title = ft.Container(
        content=ft.Text("Drive range", size=28, weight=ft.FontWeight.BOLD),
        border=ft.border.all(2),
    )

    containers = []

    for index in range(len(last_hit)):
        row = ft.Container(
            content=ft.Column([
                ft.Text(last_hit_title[index], size=35, width=180, text_align=ft.TextAlign.CENTER),
                ft.Text(last_hit[index], size=45, width=180, text_align=ft.TextAlign.CENTER),
            ]),
            padding=10,
            bgcolor="lightblue",
            border=ft.border.all(2, "black"),
            border_radius=10,
            alignment=ft.alignment.center,
            width=280,
        )
        containers.append(row)

    def selected_club(club):
        active_club["name"] = club["name"]
        active_club["image"] = club["image"]
        button.content = ft.Column([
            ft.Text(club.get("name"), size=20),
            ft.Image(src=club.get("image"), width=80, height=80),
        ])
        page.update()
        page.close(dlg_modal)

    # Создание диалога с кнопками
    dlg_modal = ft.AlertDialog(
        title=ft.Text("Выберите клюшку", size=25, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                # Создаем ряды для 3x3
                ft.Row([
                    ft.ElevatedButton(
                        width=150,
                        height=120,
                        content=ft.Column([
                            ft.Text(club["name"], size=18, text_align=ft.TextAlign.CENTER),
                            ft.Image(src=club["image"], width=75, height=75),
                        ], spacing=5),
                        on_click=lambda e, club=club: selected_club(club)
                    )
                    for club in golf_clubs[i:i + 4]  # Берем 3 элемента на каждый ряд
                ])
                for i in range(0, len(golf_clubs), 4)  # Делим на группы по 3 элемента
            ]),
            height=400,
            bgcolor=ft.Colors.BLUE,
        ),
        # height=300,  # Устанавливаем нужную высоту диалога
        # width=300,  # Устанавливаем нужную ширину
        # actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.Colors.YELLOW,
        adaptive=True,  # Сделать диалог адаптивным в зависимости от платформы
        on_dismiss=lambda e: print("Диалог закрыт")
    )

    button = ft.ElevatedButton(
        width=200,
        # height=200,
        content=ft.Column([
            ft.Text(active_club.get("name"), size=20),
            ft.Image(src=active_club.get("image"), width=80, height=80),
        ], spacing=10),
        # on_click=tess
        on_click=lambda e: page.open(dlg_modal)
    )

    containers.append(button)

    last_hit_table = ft.Container(
        content=ft.Row(
            controls=containers,
            spacing=10
        ),
        bgcolor="blue",
        padding=10,
        border_radius=15,
        # width=300,
        height=200
    )

    section = ft.Container(
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

    return section
