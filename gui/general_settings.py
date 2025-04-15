import flet as ft

from logging_config import logger

unit_system = {
    "Imperial": {"Distance": "Yards", "Speed": "mph"},
    "Metric": {"Distance": "Meters", "Speed": "km/h"},
    "Scientific": {"Distance": "Meters", "Speed": "m/s"},
}

theme_mode = ("LIGHT", "DARK")


def dropdown_changed_unit_system(value):
    logger.info(f'dropdown_changed_unit_system - value {value}')


def theme_changed(value):
    logger.info(f'theme_changed - value {value}')



async def general_set():
    dropdown_select_unit_system = ft.Dropdown(
        value="Imperial",
        on_change=dropdown_changed_unit_system,
        options=[
            ft.dropdown.Option(system) for system in unit_system.keys()
        ],
        width=150,
    )

    # dropdown_select_theme_mode = ft.Dropdown(
    #     value="LIGHT",
    #     on_change=dropdown_changed_theme_mode(),
    #     options=[
    #         ft.dropdown.Option(system) for system in unit_system.keys()
    #     ],
    #     width=150,
    # )
    c = ft.Switch(
        label="Light theme",
        on_change=theme_changed
    )

    general = ft.Container(
        content=ft.Column(
            [
                ft.Text("General"),
                # ft.Text('Language'),
                ft.Row([ft.Text('Theme:'), c]),
            ]
        ),
        bgcolor=ft.Colors.ORANGE_100,
        padding=10,
        width=200,
    )

    simulator = ft.Container(
        content=ft.Column([
            ft.Text("Units", size=20),
            dropdown_select_unit_system,
        ]),
        padding=10,
        width=200,
    )
    # graphics = ft.Container()

    return ft.Container(
        content=ft.Row(
            [
                general,
                simulator,
            ],
            spacing=20,
        ),
        bgcolor=ft.Colors.ORANGE_800,
        padding=20
    )
