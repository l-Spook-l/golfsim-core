import asyncio

import flet as ft

from .tab_home import load_home
from .tab_settings import load_settings_tab
from data_base.db import DataBase
from data_base.config_db import async_session_maker
from gui.general_settings import load_settings


async def last_shot():
    # возвращает данные о последнем выстреле (из базы данных)
    async with async_session_maker() as session:
        return await DataBase.get_last_shot(session=session)


async def main(page: ft.Page) -> None:
    page.title = "GolfMonitor"
    # Устанавливаем размер окна и позиционируем его по центру
    page.window.width = 1800
    page.window.height = 900
    page.padding = 0

    theme = await load_settings()

    page.theme_mode = ft.ThemeMode.DARK if theme["theme"] == "dark" else ft.ThemeMode.LIGHT

    home = await load_home(page)
    settings = await load_settings_tab(page)

    # Контейнер для отображения текущего содержимого
    content_container = ft.Container(
        bgcolor=ft.Colors.YELLOW_200,
        padding=10,
        width=1550
    )

    # Функция для загрузки контента в зависимости от выбранного пункта меню
    async def load_menu_content(menu_index):
        # Загрузка контента в зависимости от выбранного пункта меню
        match menu_index:
            case 0:
                content_container.content = home
            case 1:
                content_container.content = settings

        content_container.update()

    # Функция для обработки изменения выбранного пункта в навигации
    async def on_nav_change(e):
        await load_menu_content(nav.selected_index)
        update_navigation_rail(nav.selected_index)

    def update_navigation_rail(active_index):
        """Обновляет боковое меню, делая активный пункт неактивным."""
        nonlocal nav
        nav.destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.HOME, size=30),
                selected_icon=ft.Icon(ft.Icons.HOME, size=38),
                label="Home",
                disabled=active_index == 0  # Отключаем, если активен
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_SUGGEST_OUTLINED,
                label="Settings",
                disabled=active_index == 1
            ),
        ]
        page.padding = 0
        page.update()

    # Боковое меню
    nav = ft.NavigationRail(
        selected_index=0,
        destinations=[],
        on_change=on_nav_change,
        width=100,
        bgcolor=ft.Colors.LIGHT_GREEN_ACCENT_200
    )

    update_navigation_rail(0)

    # Функция для проверки базы данных и обновления флага
    async def check_db_for_updates():
        last_shot_data = await last_shot()
        while True:
            # Проверяем, изменились ли данные в базе
            new_shot_data = await last_shot()
            if new_shot_data != last_shot_data:
                content_container.content = None
                content_container.update()

                content_container.content = await load_home(page)
                content_container.update()
                last_shot_data = new_shot_data  # Обновляем данные последнего выстрела
            await asyncio.sleep(5)  # Пауза между проверками

    # Основная компоновка: меню слева, контент справа
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    nav,
                    ft.VerticalDivider(width=1),
                    content_container,
                ],
            ),
            expand=True,
            bgcolor=ft.Colors.BLUE_400,
        )
    )

    # Стартуем фоновую проверку базы данных
    asyncio.ensure_future(check_db_for_updates())

    # Загружаем содержимое первого пункта меню (Home)
    await load_menu_content(0)


async def start_flet():
    await ft.app_async(target=main)
