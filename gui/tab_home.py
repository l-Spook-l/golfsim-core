import flet as ft

from gui.drive_range_section import load_drive_range_section


async def load_home(page: ft.Page) -> ft.Container:
    current_view = ft.Container()

    drive_range = await load_drive_range_section(page)

    def build_card(route_target: str, image_url: str) -> ft.Container:
        return ft.Container(
            content=ft.Image(
                src=image_url,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(8),
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_100,
            expand=True,
            margin=10,
            ink=True,
            on_click=lambda e: update_view(route_target)
        )
    button_return_home = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: show_home())

    def show_home():
        current_view.content = home
        current_view.update()

    def header_selected_section(section):
        return ft.Container(
            content=ft.Text(section, size=28, weight=ft.FontWeight.BOLD),
        )

    def update_view(route: str):
        match route:
            case "/drive-range":
                current_view.content = ft.Column([
                    ft.Row([
                        button_return_home,
                        header_selected_section("Drive range")
                    ]),
                    drive_range
                ])
            case "/putting":
                current_view.content = ft.Column([
                    button_return_home,
                    ft.Text("🎯 Putting view", size=30)
                ])
            case "/play-course":
                current_view.content = ft.Column([
                    button_return_home,
                    ft.Text("⛳ Play Course view", size=30)
                ])
        current_view.update()

    home = ft.Container(
        content=ft.Row(
            controls=[
                build_card("/drive-range", "menu/drive-range.png"),
                build_card("/putting", "menu/putting.png"),
                build_card("/play-course", "menu/play-course.png"),
            ],
            expand=True,
            spacing=0
        ),
        expand=True
    )

    current_view.content = home

    return current_view
