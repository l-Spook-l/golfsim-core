import os
import json

import flet as ft

from states.shot_state import ShotState
from states.app_page_state import PageState
from data_base.schemas import LastGolfShotSchema
from gui.drive_range_dashboard import DriveRangeDashboard
from logging_config import logger


class LastShotSection:
    def __init__(self, last_shot: dict):
        self.page = PageState.get_page()
        self.last_shot = last_shot
        self.active_club = {"name": "", "image": ""}
        self.golf_clubs = {}
        self.dlg_modal = ft.AlertDialog()
        self.button_select_club = None
        self.shot_selected_club = ShotState()
        self.drive_range_dashboard = DriveRangeDashboard()

    async def load_clubs_info(self):
        if os.path.exists("data/clubs.json"):
            with open("data/clubs.json", "r", encoding="utf-8") as file:
                try:
                    self.golf_clubs = json.load(file)
                except json.JSONDecodeError:
                    logger.info("File is corrupted. Creating it again.")
        name_active_club = self.shot_selected_club.club
        self.active_club = {
            "name": name_active_club,
            "image": self.golf_clubs.get(name_active_club).get("image")
        }

    def update_selected_club(self, club_name: str, club_image_src: str):
        self.active_club["name"] = club_name
        self.active_club["image"] = club_image_src
        self.button_select_club.content = ft.Column([
            ft.Text(club_name, size=20),
            ft.Image(src=club_image_src, width=80, height=80),
        ])
        self.shot_selected_club.club = club_name
        self.shot_selected_club.save()
        self.page.close(self.dlg_modal)
        self.page.update()

    def build_club_selector(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            title=ft.Text("Choose a club", size=25, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.ElevatedButton(
                            width=150,
                            height=120,
                            content=ft.Column([
                                ft.Text(f"{club[0]}", size=18),
                                ft.Image(src=club[1].get("image"), width=75, height=75),
                            ], spacing=5),
                            on_click=lambda e, club_name=club[0],
                                            club_image_src=club[1].get("image"): self.update_selected_club(
                                club_name, club_image_src)
                        )
                        for club in list(self.golf_clubs.items())[i:i + 4]
                    ])
                    for i in range(0, len(self.golf_clubs), 4)
                ]),
                height=400,
            ),
            bgcolor="#E4E7EB",
            # adaptive=True,  # Сделать диалог адаптивным в зависимости от платформы
            on_dismiss=lambda e: print("Диалог закрыт")
        )

    def build_last_shot_table(self) -> ft.Container:
        last_shot_data = []
        for field_name, field_value in LastGolfShotSchema.model_fields.items():
            title = field_value.title
            value = self.last_shot.get(field_name)
            row = ft.Container(
                content=ft.Column([
                    ft.Text(title, size=35, width=180, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"{value}", size=45, width=180, text_align=ft.TextAlign.CENTER),
                ]),
                bgcolor="#E8F5E9",
                border=ft.border.all(1, "black"),
                border_radius=10,
                alignment=ft.alignment.center,
                width=280,
            )
            last_shot_data.append(row)

        self.button_select_club = ft.ElevatedButton(
            width=200,
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
            height=200
        )

    async def build_section(self) -> ft.Container:
        await self.load_clubs_info()
        self.dlg_modal = self.build_club_selector()
        last_shot_table = self.build_last_shot_table()
        load_drive_range_dashboard = DriveRangeDashboard()
        self.drive_range_dashboard = await load_drive_range_dashboard.build_section()

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=last_shot_table,
                ),
            ]),
        )
