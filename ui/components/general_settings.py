import os
import json

import flet as ft
import aiofiles

from states.app_page_state import PageState
from data_base.config_db import async_session_maker
from data_base.models import HSVSetting
from data_base.repositories.hsv_setting import HSVSettingRepository
from core.utils import load_settings
from core.logging_config import logger


class GeneralSettings:
    """
    Class for managing general application settings.

    Main functionality:
    - Switching theme (light/dark).
    - Selecting unit system (imperial, metric, scientific).
    - Managing HSV settings:
        • loading profiles,
        • activation and deletion,
        • displaying the active profile,
        • updating the UI after changes.

    Attributes:
        page (PageState): current Flet page object.
        unit_system (dict): dictionary of unit system options.
        theme_mode (tuple): available theme options ("LIGHT", "DARK").
        container_section (ft.Container): container for the main settings block.
        active_hsv_set (ft.Container): container for the active HSV set.
        dlg_modal (ft.AlertDialog): modal window for HSV set selection.
        hsv_sets_data (list | None): list of inactive HSV sets.
    """

    def __init__(self):
        self.page = PageState.get_page()
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
        """
        Saves a setting to a JSON file.

        Args:
            field (str): Name of the field (e.g., "theme" or "units").
            value (str): New value to save.
            file_path (str): Path to the settings file.
        """
        data = await load_settings()
        data[field] = value
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4))
        logger.info(f"Theme updated: {value}")

    @classmethod
    async def change_unit_system(cls, value: ft.ControlEvent):
        """
        Changes the unit system and saves it to JSON.

        Args:
            value (ft.ControlEvent): Dropdown selection event.
        """
        units_value = value.data
        logger.info(f'dropdown_changed_unit_system - value {value}')
        await cls.save_to_json('units', units_value)

    @classmethod
    async def change_theme(cls, value: ft.ControlEvent):
        """
        Changes the theme (light/dark) and saves it to JSON.

        Args:
            value (ft.ControlEvent): Switch toggle event.
        """
        theme_value = "dark" if value.data == "true" else "light"
        logger.info(f'theme_changed - value {value}, {theme_value}')
        await cls.save_to_json('theme', theme_value)

    async def load_hsv_sets(self):
        """
        Loads the list of inactive HSV profiles from the database.
        """
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            self.hsv_sets_data = await repo.get_inactive_hsv_sets()

    async def hvs_selector(self):
        """
        Creates a dialog window for selecting and managing HSV profiles.

        Returns:
            ft.AlertDialog: a dialog containing HSV profile cards.
        """
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
                                            on_click=lambda e, hsv_id=hsv_data.id, photo_name=hsv_data.photo:
                                            self.page.run_task(self.delete_hsv_set, hsv_id, photo_name)
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
                                            src=hsv_data.photo,
                                            fit=ft.ImageFit.COVER,
                                            width=200,
                                            height=200,
                                            border_radius=5
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ])
                        ) for hsv_data in self.hsv_sets_data[i:i + 4]
                    ]) for i in range(0, len(self.hsv_sets_data), 4)
                ])
            ),
            bgcolor="#E4E7EB",
            on_dismiss=lambda e: print("Диалог закрыт")
        )

    async def change_active_hsv_set(self, hsv_id: int):
        """
        Activates the selected HSV profile.

        Args:
            hsv_id (int): ID of the HSV profile.
        """
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            await repo.set_active_hsv_set(hsv_id)
        await self.refresh_after_hsv_change()

    async def delete_hsv_set(self, hsv_id: int, photo_name: str):
        """
        Deletes an HSV profile and its associated image.

        Args:
            hsv_id (int): ID of the HSV profile.
            photo_name (str): Path to the profile image.
        """
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            await repo.delete_by_id(HSVSetting, hsv_id)
        if os.path.exists(photo_name):
            os.remove(photo_name)
        await self.refresh_after_hsv_change()

    async def refresh_after_hsv_change(self):
        """
        Updates the UI after changing the active HSV profile
        (either switching or deleting it).
        """
        self.active_hsv_set = await self.get_active_hsv_set()
        self.hsv_sets_data = await self.load_hsv_sets()
        self.container_section.content.controls[1] = self.active_hsv_set
        self.container_section.update()
        self.page.close(self.dlg_modal)
        self.dlg_modal = await self.hvs_selector()

    async def get_active_hsv_set(self) -> ft.Container:
        """
        Gets the active HSV profile from the database (or creates a default one if not found).

        Returns:
            ft.Container: UI block containing the active HSV profile.
        """
        async with async_session_maker() as session:
            repo = HSVSettingRepository(session)
            data = await repo.get_active_hsv_set()
            if not data:
                data = await repo.create_default_hsv()

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
            src=data.photo,
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
        """
        Assembles the UI section for general settings:
        - theme selection
        - unit system selection
        - active HSV profile

        Returns:
            ft.Container: the ready UI interface section.
        """
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

        theme = ft.Container(
            content=ft.Row([
                ft.Text('Theme:', size=20),
                ft.Switch(
                    on_change=self.change_theme
                )
            ]),
            padding=10,
            width=200,
            bgcolor="#E4E7EB",
            border_radius=10
        )

        simulator = ft.Container(
            content=ft.Column([
                ft.Text("Units", size=20),
                dropdown_select_unit_system,
            ]),
            padding=10,
            width=200,
            bgcolor="#E4E7EB",
            border_radius=10
        )

        self.container_section = ft.Container(
            content=ft.Row(
                [
                    ft.Column([
                        theme,
                        simulator,
                    ]),
                    self.active_hsv_set
                ],
                spacing=20,
            ),
            padding=20
        )

        return self.container_section
