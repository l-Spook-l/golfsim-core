import asyncio

import flet as ft

from gui.app_context import AppContext
from gui.tab_home import HomeView
from gui.tab_settings import SettingsView
from utils import load_settings


async def app(page: ft.Page) -> None:
    AppContext.set_page(page)
    page.title = "GolfSim"
    page.window.maximized = True
    page.window.min_width = 680
    page.window.min_height = 420
    page.bgcolor = "#F4F4F6"
    page.padding = 0

    theme = await load_settings()
    page.theme_mode = ft.ThemeMode.DARK if theme["theme"] == "dark" else ft.ThemeMode.LIGHT

    home_view = HomeView()
    home = await home_view.init()

    settings_view = SettingsView()
    settings = await settings_view.init()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            ft.Tab(
                icon=ft.Icon(ft.Icons.HOME, size=35),
                content=home,
            ),
            ft.Tab(
                icon=ft.Icon(ft.Icons.SETTINGS, size=35),
                content=settings,
            ),
        ],
        tab_alignment=ft.TabAlignment.CENTER,
        expand=1,
    )

    async def handle_window_event(e):
        if e.data == "close":
            page.window.destroy()

    # TODO: Add a button to exit and close the application
    # exit_button = ft.IconButton(
    #     icon=ft.Icons.EXIT_TO_APP,
    #     on_click=lambda e: page.window.close(),
    #     icon_size=35,
    #     tooltip="Закрыть приложение",
    # )

    page.window.on_event = handle_window_event
    page.add(tabs)


async def start_flet(shutdown_event: asyncio.Event = None):
    try:
        await ft.app_async(
            target=app,
            assets_dir="assets",
            view=ft.FLET_APP
        )
    finally:
        if shutdown_event:
            shutdown_event.set()
