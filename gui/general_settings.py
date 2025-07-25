import os
import json

import flet as ft
import aiofiles

from data_base.config_db import async_session_maker
from data_base.db import DataBase
from data_base.models import HSVSetting
from utils import load_settings
from logging_config import logger


class GeneralSettings:
    def __init__(self):
        self.unit_system = {
            "Imperial": {"Distance": "Yards", "Speed": "mph"},
            "Metric": {"Distance": "Meters", "Speed": "km/h"},
            "Scientific": {"Distance": "Meters", "Speed": "m/s"},
        }

        self.theme_mode = ("LIGHT", "DARK")

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
    async def dropdown_changed_unit_system(cls, value):
        units_value = value.data
        logger.info(f'dropdown_changed_unit_system - value {value}')
        await cls.save_to_json('units', units_value)

    @classmethod
    async def theme_changed(cls, value):
        theme_value = "dark" if value.data == "true" else "light"
        logger.info(f'theme_changed - value {value}, {theme_value}')
        await cls.save_to_json('theme', theme_value)

    async def active_profile_change(self):
        async with async_session_maker() as session:
            data = await DataBase.get_active_profile(session, HSVSetting)
            logger.info(f"Data active_hsv - {data.id}")

        return ft.Container(

        )

    async def build_section(self):
        dropdown_select_unit_system = ft.Dropdown(
            value="Imperial",
            on_change=self.dropdown_changed_unit_system,
            options=[
                ft.dropdown.Option(system) for system in self.unit_system.keys()
            ],
            width=150,
        )

        c = ft.Switch(
            label="Light theme",
            on_change=self.theme_changed
        )

        general = ft.Container(
            content=ft.Column(
                [
                    ft.Text("General"),
                    # ft.Text('Language'),
                    ft.Row([ft.Text('Theme:'), c]),
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

        return ft.Container(
            content=ft.Row(
                [
                    general,
                    simulator,
                ],
                spacing=20,
            ),
            bgcolor=ft.Colors.ORANGE_800,
            padding=20
        )
