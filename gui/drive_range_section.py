import os
import json

import flet as ft

from gui.tab_graph import load_stat
from logging_config import logger


class DriveRangeSection:
    def __init__(self, page: ft.Page, last_shot: list):
        self.page = page
        self.last_shot = last_shot
        self.active_club = {"name": "", "image": ""}
        self.golf_clubs = []
        self.dlg_modal = None
        self.button_select_club = None
        self.last_hit_title = ("Carry (yd)", "Ball (mph)", "Launch V", "Launch H")

    async def load_clubs_info(self):
        if os.path.exists("data/clubs.json"):
            with open("data/clubs.json", "r", encoding="utf-8") as f:
                try:
                    self.golf_clubs = json.load(f)['clubs']
                except json.JSONDecodeError:
                    logger.info("File is corrupted. Creating it again.")
        # logger.info(f'path - {os.path.exists("settings.json")}')
        # logger.info(f'data - {data}')
        self.active_club = {
            "name": self.golf_clubs[0]["name"],
            "image": self.golf_clubs[0]["image"]
        }

    def update_selected_club(self, club):
        self.active_club["name"] = club["name"]
        self.active_club["image"] = club["image"]
        self.button_select_club.content = ft.Column([
            ft.Text(club.get("name"), size=20),
            ft.Image(src=club.get("image"), width=80, height=80),
        ])
        logger.info(f"Selected {club} club")
        self.page.update()
        self.page.close(self.dlg_modal)

    def build_club_selector(self) -> ft.AlertDialog:
        # Создание диалога с кнопками
        return ft.AlertDialog(
            title=ft.Text("Choose a club", size=25, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column([
                    # Создаем ряды для NxM
                    ft.Row([
                        ft.ElevatedButton(
                            width=150,
                            height=120,
                            content=ft.Column([
                                ft.Text(club["name"], size=18),
                                ft.Image(src=club["image"], width=75, height=75),
                            ], spacing=5),
                            on_click=lambda e, club=club: self.update_selected_club(club)
                        )
                        for club in self.golf_clubs[i:i + 4]  # Берем 3 элемента на каждый ряд
                    ])
                    for i in range(0, len(self.golf_clubs), 4)  # Делим на группы по 3 элемента
                ]),
                height=400,
                # bgcolor="#007AFF",
            ),
            # height=300,
            # width=300,
            # actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#E4E7EB",
            adaptive=True,  # Сделать диалог адаптивным в зависимости от платформы
            on_dismiss=lambda e: print("Диалог закрыт")
        )
        # return self.dlg_modal

    def build_last_shot_table(self) -> ft.Container:
        last_shot_data = []
        for index in range(len(self.last_shot)):
            row = ft.Container(
                content=ft.Column([
                    ft.Text(self.last_hit_title[index], size=35, width=180, text_align=ft.TextAlign.CENTER),
                    ft.Text(self.last_shot[index], size=45, width=180, text_align=ft.TextAlign.CENTER),
                ]),
                # padding=10,
                bgcolor="#E8F5E9",
                border=ft.border.all(1, "black"),
                border_radius=10,
                alignment=ft.alignment.center,
                width=280,
            )
            last_shot_data.append(row)

        self.button_select_club = ft.ElevatedButton(
            width=200,
            # height=200,
            content=ft.Column([
                ft.Text(self.active_club.get("name"), size=20, text_align=ft.TextAlign.CENTER),
                ft.Image(src=self.active_club.get("image"), width=80, height=80),
            ], spacing=10),
            bgcolor="#E8F5E9",
            on_click=lambda e: self.page.open(self.dlg_modal)
        )

        last_shot_data.append(self.button_select_club)

        return ft.Container(
            content=ft.Row(
                controls=last_shot_data,
                spacing=10
            ),
            bgcolor="#C8E6C9",
            padding=10,
            border_radius=15,
            # width=300,
            height=200
        )

    async def build_section(self) -> ft.Container:
        await self.load_clubs_info()
        self.dlg_modal = self.build_club_selector()
        last_shot_table = self.build_last_shot_table()
        stats_graph = await load_stat(self.page)

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=last_shot_table,
                    # bgcolor="#E1F0FF"
                ),
                ft.Container(
                    content=stats_graph,
                    # bgcolor=ft.Colors.ORANGE_100
                ),
            ]),
            # bgcolor=ft.Colors.GREEN_ACCENT_100
        )
