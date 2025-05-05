import os
import json

import flet as ft
import aiofiles
from logging_config import logger

unit_system = {
    "Imperial": {"Distance": "Yards", "Speed": "mph"},
    "Metric": {"Distance": "Meters", "Speed": "km/h"},
    "Scientific": {"Distance": "Meters", "Speed": "m/s"},
}

theme_mode = ("LIGHT", "DARK")


async def load_settings():
    # 1. Прочитать файл, если он существует
    if os.path.exists("Settings.json"):
        async with aiofiles.open("Settings.json", "r", encoding="utf-8") as f:
            try:
                data = json.loads(await f.read())
            except json.JSONDecodeError:
                print("⚠️ Файл пустой или повреждён. Создаём заново.")
    return data


async def save_to_json(field: str, value: str, file_path: str = "Settings.json"):
    # 1. Прочитать файл, если он существует
    data = await load_settings()
    # 2. Изменяем только нужное значение
    data[field] = value
    # 3. Записываем измененные данные обратно в файл
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=4))
    logger.info(f"Тема обновлена: {value}")


async def dropdown_changed_unit_system(value):
    units_value = value.data
    logger.info(f'dropdown_changed_unit_system - value {value}')
    await save_to_json('units', units_value)


async def theme_changed(value):
    theme_value = "dark" if value.data == "true" else "light"
    logger.info(f'theme_changed - value {value}, {theme_value}')
    await save_to_json('theme', theme_value)


async def general_set():
    dropdown_select_unit_system = ft.Dropdown(
        value="Imperial",
        on_change=dropdown_changed_unit_system,
        options=[
            ft.dropdown.Option(system) for system in unit_system.keys()
        ],
        width=150,
    )

    # dropdown_select_theme_mode = ft.Dropdown(
    #     value="LIGHT",
    #     on_change=dropdown_changed_theme_mode(),
    #     options=[
    #         ft.dropdown.Option(system) for system in unit_system.keys()
    #     ],
    #     width=150,
    # )
    c = ft.Switch(
        label="Light theme",
        on_change=theme_changed
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
    # graphics = ft.Container()

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
