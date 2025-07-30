import json

import flet as ft
import aiofiles

from data_base.config_db import async_session_maker
from data_base.models import HSVSetting
from data_base.repositories.hsv_setting import HSVSettingRepository
from gui.app_context import AppContext
from utils import load_settings
from logging_config import logger


class GeneralSettings:
    def __init__(self):
        self.page = AppContext.get_page()
        self.unit_system = {
            "Imperial": {"Distance": "Yards", "Speed": "mph"},
            "Metric": {"Distance": "Meters", "Speed": "km/h"},
            "Scientific": {"Distance": "Meters", "Speed": "m/s"},
        }
        self.theme_mode = ("LIGHT", "DARK")
        self.container_section = ft.Container()
        self.active_hsv_set = ft.Container()
        self.dlg_modal = ft.AlertDialog()
        self.hsv_sets_data = None

    @classmethod
    async def save_to_json(cls, field: str, value: str, file_path: str = "settings.json"):
        # 1. Прочитать файл, если он существует
        data = await load_settings()
        # 2. Изменяем только нужное значение
        data[field] = value
        # 3. Записываем измененные данные обратно в файл
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4))
        logger.info(f"Theme updated: {value}")

    @classmethod
    async def change_unit_system(cls, value):
        units_value = value.data
        logger.info(f'dropdown_changed_unit_system - value {value}')
        await cls.save_to_json('units', units_value)

    @classmethod
    async def change_theme(cls, value):
        theme_value = "dark" if value.data == "true" else "light"
        logger.info(f'theme_changed - value {value}, {theme_value}')
        await cls.save_to_json('theme', theme_value)

    async def load_hsv_sets(self):
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            self.hsv_sets_data = await repo.get_all_hsv_set()

    async def hvs_selector(self):
        await self.load_hsv_sets()
        return ft.AlertDialog(
            title=ft.Text("Choose a HSV set", size=25, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            width=350,
                            height=280,
                            border_radius=15,
                            padding=10,
                            bgcolor="white",
                            content=ft.Column([
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.SPELLCHECK_ROUNDED,
                                            icon_color="green",
                                            on_click=lambda e, hsv_id=hsv_data.id: self.page.run_task(
                                                self.change_active_hsv_set, hsv_id)
                                        ),
                                        ft.Text(f"{hsv_data.profile_name}", size=22),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                                            icon_color="red",
                                            on_click=lambda e, hsv_id=hsv_data.id: self.page.run_task(
                                                self.delete_hsv_set, hsv_id)
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Row(
                                    [
                                        ft.Column([
                                            ft.Text(f"hmin: {hsv_data.hue_min}", size=18),
                                            ft.Text(f"hmax: {hsv_data.saturation_min}", size=18),
                                            ft.Text(f"smin: {hsv_data.value_min}", size=18),
                                            ft.Text(f"smax: {hsv_data.hue_max}", size=18),
                                            ft.Text(f"vmin: {hsv_data.saturation_max}", size=18),
                                            ft.Text(f"vmax: {hsv_data.hue_max}", size=18),
                                        ]),
                                        ft.Image(
                                            src="mobile_uploads/images/profile_images/photo.jpg",
                                            fit=ft.ImageFit.COVER,
                                            width=200,
                                            height=200,
                                            border_radius=5
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ])
                        ) for hsv_data in self.hsv_sets_data[i:i + 4] if not hsv_data.is_active
                    ]) for i in range(0, len(self.hsv_sets_data), 4)
                ])
            ),
            bgcolor="#E4E7EB",
            on_dismiss=lambda e: print("Диалог закрыт")
        )

    async def change_active_hsv_set(self, hsv_id: int):
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            await repo.set_active_hsv_set(hsv_id)
        await self.refresh_after_hsv_change()

    async def delete_hsv_set(self, hsv_id: int):
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            await repo.delete_by_id(HSVSetting, hsv_id)
        await self.refresh_after_hsv_change()

    async def refresh_after_hsv_change(self):
        self.active_hsv_set = await self.get_active_hsv_set()
        self.hsv_sets_data = await self.load_hsv_sets()
        self.container_section.content.controls[2] = self.active_hsv_set
        self.container_section.update()
        self.page.close(self.dlg_modal)
        self.dlg_modal = await self.hvs_selector()

    async def get_active_hsv_set(self) -> ft.Container:
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            data = await repo.get_active_hsv_set()
            logger.info(f"Data active_hsv - {data.id}")

        info_section = ft.Column(
            [
                ft.Column([
                    ft.Text(f"hmin: {data.hue_min}", size=18),
                    ft.Text(f"hmax: {data.saturation_min}", size=18),
                    ft.Text(f"smin: {data.value_min}", size=18),
                    ft.Text(f"smax: {data.hue_max}", size=18),
                    ft.Text(f"vmin: {data.saturation_max}", size=18),
                    ft.Text(f"vmax: {data.hue_max}", size=18),
                ])
            ]
        )

        image_section = ft.Image(
            src="mobile_uploads/images/profile_images/photo.jpg",
            fit=ft.ImageFit.COVER,
            width=200,
            height=200,
            border_radius=5
        )

        button_change_active_hsv = ft.ElevatedButton(
            text="Change active HSV set",
            on_click=lambda e: self.page.open(self.dlg_modal)
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(f"Active HSV", size=25, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [
                        ft.Text(f"{data.profile_name}", size=22),
                        button_change_active_hsv
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [info_section, image_section],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]),
            bgcolor="#E4E7EB",
            width=350,
            height=320,
            padding=10,
            border_radius=10,
        )

    async def build_section(self) -> ft.Container:
        self.dlg_modal = await self.hvs_selector()
        self.active_hsv_set = await self.get_active_hsv_set()

        dropdown_select_unit_system = ft.Dropdown(
            value="Imperial",
            on_change=self.change_unit_system,
            options=[
                ft.dropdown.Option(system) for system in self.unit_system.keys()
            ],
            width=150,
        )

        general = ft.Container(
            content=ft.Column(
                [
                    ft.Text("General"),
                    ft.Row([
                        ft.Text('Theme:'),
                        ft.Switch(
                            on_change=self.change_theme
                        )
                    ]),
                ]
            ),
            bgcolor=ft.Colors.ORANGE_100,
            padding=10,
            width=200,
        )

        simulator = ft.Container(
            content=ft.Column([
                ft.Text("Units", size=20),
                dropdown_select_unit_system,
            ]),
            padding=10,
            width=200,
        )

        self.container_section = ft.Container(
            content=ft.Row(
                [
                    ft.Column([
                        general,
                        simulator,
                    ]),
                    self.active_hsv_set
                ],
                spacing=20,
            ),
            bgcolor=ft.Colors.ORANGE_800,
            padding=20
        )

        return self.container_section
