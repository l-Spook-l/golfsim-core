import asyncio

import flet as ft

from .tab_home import load_home
from .tab_settings import load_settings
from data_base.db import DataBase
from data_base.config_db import async_session_maker


async def last_shot():
    # возвращает данные о последнем выстреле (из базы данных)
    async with async_session_maker() as session:
        return await DataBase.get_last_shot(session=session)


async def main(page: ft.Page) -> None:
    # Устанавливаем размер окна и позиционируем его по центру
    page.window.width = 1800
    page.window.height = 900
    page.padding = 0

    home = await load_home(page)
    settings = await load_settings(page)

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

        page.update()

    # Боковое меню
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.QUERY_STATS, label="Statistic"),
            ft.NavigationRailDestination(icon=ft.Icons.TERMINAL, label="For"),
        ],
        on_change=lambda e: load_menu_content(nav_rail.selected_index),
    )

    # Основная компоновка: меню слева, контент справа
    page.add(
        ft.Row(
            [
                nav_rail,
                content_container,
            ],
            expand=True,
        )
    )

    # Загружаем содержимое первого пункта меню
    load_menu_content(0)

    # Загружаем содержимое первого пункта меню (Home)
    await load_menu_content(0)


async def start_flet():
    await ft.app_async(target=main)
