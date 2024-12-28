# import flet as ft
#
#
# def main_1(page):
#     def add_clicked(e):
#         page.add(ft.Checkbox(label=new_task.value))
#         new_task.value = ""
#         new_task.focus()
#         new_task.update()
#
#     new_task = ft.TextField(hint_text="Whats needs to be done?", width=300)
#     page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))
#
#
# if __name__ == "__main__":
#     ft.app(target=main_1, view=ft.WEB_BROWSER)
import flet as ft


def load_tab_1(page: ft.Page):
    new_task = ft.TextField(hint_text="What needs to be done?", width=300)

    def add_clicked(e):
        tasks.controls.append(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        page.update()

    tasks = ft.Column()

    return ft.Column(
        [
            ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]),
            tasks,
        ]
    )
