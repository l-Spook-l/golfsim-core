import asyncio

import flet as ft

from gui.find_color import load_hsv_tab
from gui.find_point import load_find_distance_point
from gui.general_settings import general_set


class SettingsView:
    def __init__(self):
        self.tabs = ft.Tabs()
        self.content_container = ft.Container()
        self.settings = ft.Container()
        self.current_tab = None

    async def on_tab_change(self, e):
        match self.tabs.selected_index:
            case 0:
                self.current_tab = await general_set()
            case 1:
                self.current_tab = await load_hsv_tab()
            case 2:
                self.current_tab = await load_find_distance_point()

        self.content_container.content = self.current_tab
        self.content_container.update()

    async def init(self) -> ft.Container:
        self.tabs = ft.Tabs(
            selected_index=0,
            on_change=lambda e: asyncio.create_task(self.on_tab_change(e)),
            tabs=[
                ft.Tab(text="General settings"),
                ft.Tab(text="Find ball's color"),
                ft.Tab(text="Find pixel distance on screen"),
            ],
        )

        self.content_container = ft.Container(
            content=await general_set(),
            # width=500,
            # height=500,
            bgcolor="red"
        )

        self.settings = ft.Container(
            content=ft.Column(
                [
                    self.tabs,
                    self.content_container
                ]
            )
        )
        return self.settings

    return tab_content

#     page.add(tabs, tab_content)
#
# ft.app(target=main)
