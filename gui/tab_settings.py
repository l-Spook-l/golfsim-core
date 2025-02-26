import flet as ft
from .find_color import load_hsv_tab


def load_settings(page: ft.Page):
    page.title = "Tabs Example"

    def on_tab_change(e):
        print('tabs.selected_index - ', tabs.selected_index)
        tab_content.clean()
        match tabs.selected_index:
            case 0:
                tab_content.content = (ft.Text("Содержимое Вкладки 1"))
            case 1:
                tab_content.content = load_hsv_tab(page)
            case 2:
                tab_content.content = (ft.Text("Содержимое Вкладки 3"))
        tab_content.update()

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

    tab_content = ft.Container(
        content=(ft.Text("Содержимое Вкладки 1")),
        # width=500,
        # height=500,
        bgcolor="red"
    )

    return ft.Column(
        [
            tabs,
            tab_content
        ]
    )

#     page.add(tabs, tab_content)
#
# ft.app(target=main)
