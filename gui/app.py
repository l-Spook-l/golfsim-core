""" Меню слева """
import flet as ft
from tab_1 import load_tab_1
from tab_2 import load_tab_2


def main(page: ft.Page):
    # Устанавливаем размер окна и позиционируем его по центру
    page.window.width = 1800
    page.window.height = 900
    page.padding = 0

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
                content_container.content = await load_home(page)
            case 1:
                content_container.content = await load_settings(page)

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


if __name__ == "__main__":
    ft.app(target=main)
