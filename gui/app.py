import flet as ft

from gui.tab_home import HomeView
from gui.tab_settings import SettingsView
from gui.general_settings import load_settings


async def main(page: ft.Page) -> None:
    page.title = "GolfSim"

    page.window.maximized = True

    # Устанавливаем размер окна и позиционируем его по центру
    page.window.width = 1700
    page.window.height = 900
    page.window.min_width = 680  # Минимальная ширина окна
    page.window.min_height = 420  # Минимальная высота окна
    page.bgcolor = "#F4F4F6"
    page.padding = 0

    theme = await load_settings()
    page.theme_mode = ft.ThemeMode.DARK if theme["theme"] == "dark" else ft.ThemeMode.LIGHT

    home_view = HomeView(page)
    home = await home_view.init()

    settings_view = SettingsView()  # создаёшь объект
    settings = await settings_view.init()  # получаешь визуальный элемент (Container)

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

    button_exit_app = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        on_click=lambda e: page.window.destroy(),
        icon_size=35
    )

    page.add(tabs)


async def start_flet():
    await ft.app_async(target=main, assets_dir="assets")