import flet as ft
from .find_color import load_hsv_tab
from .find_point import load_find_distance_point


async def load_settings(page: ft.Page):
    page.title = "Settings"

    async def on_tab_change(e):
        print('tabs.selected_index - ', tabs.selected_index)

        current_tab = None
        match tabs.selected_index:
            case 0:
                current_tab = (ft.Text("Содержимое Вкладки 1"))
            case 1:
                current_tab = await load_hsv_tab()
            case 2:
                current_tab = await load_find_distance_point()

        settings_container.content = current_tab
        settings_container.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(text="Вкл1"),
            ft.Tab(text="Find ball's color"),
            ft.Tab(text="Find pixel distance on screen"),
        ],
        # expand=1,
    )

    settings_container = ft.Container(
        content=(ft.Text("Содержимое Вкладки 1")),
        # width=500,
        # height=500,
        bgcolor="red"
    )

    tab_content = ft.Column(
        [
            tabs,
            settings_container
        ]
    )

    return tab_content

#     page.add(tabs, tab_content)
#
# ft.app(target=main)
