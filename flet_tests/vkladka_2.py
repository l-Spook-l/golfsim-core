# import flet as ft
#
#
# def main_2(page):
#     first_name = ft.TextField(label="First name", autofocus=True)
#     last_name = ft.TextField(label="Last name")
#     greetings = ft.Column()
#
#     def btn_click(e):
#         greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
#         first_name.value = ""
#         last_name.value = ""
#         page.update()
#         first_name.focus()
#
#     page.add(
#         first_name,
#         last_name,
#         ft.ElevatedButton("Say hello!", on_click=btn_click),
#         greetings,
#     )
#
#
# if __name__ == "__main__":
#     ft.app(target=main_2, view=ft.WEB_BROWSER)
import flet as ft


def load_tab_2(page: ft.Page):
    first_name = ft.TextField(label="First name", autofocus=True)
    last_name = ft.TextField(label="Last name")
    greetings = ft.Column()

    def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
        first_name.value = ""
        last_name.value = ""
        page.update()
        first_name.focus()

    return ft.Column(
        [
            first_name,
            last_name,
            ft.ElevatedButton("Say hello!", on_click=btn_click),
            greetings,
        ]
    )
