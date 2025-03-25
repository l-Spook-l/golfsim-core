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
        ft.Row(
            [
                nav_rail,
                content_container,
            ],
            expand=True,
        )
    )

    # Стартуем фоновую проверку базы данных
    asyncio.ensure_future(check_db_for_updates())

    # Загружаем содержимое первого пункта меню (Home)
    await load_menu_content(0)


async def start_flet():
    await ft.app_async(target=main)
