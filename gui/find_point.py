import flet as ft
import flet.canvas as cv
from PIL import Image


# Класс для хранения состояния
class State:
    shapes = []  # Список для хранения точек


state = State()


# image_path = "../video_dnerp/ball 240 2024-07-27 141246.png"
# img = Image.open(image_path)  # Открываем изображение
#
# width, height = img.size  # Получаем ширину и высоту
#
# print(f"Ширина: {width}, Высота: {height}")


async def load_find_distance_point():
    # page.title = "Flet Brush with Points"

    distance_px_value = 0

    # Функция для обработки клика
    def mouse_test(e):
        nonlocal distance_px_value
        x, y = int(e.local_x), int(e.local_y)
        print(f"Клик по координатам: {x}, {y}")
        print(f"sdaaaaaa", state.shapes)
        if len(state.shapes) >= 2:
            state.shapes.clear()

        # Добавляем новую точку
        state.shapes.append(
            cv.Circle(x, y, 8, paint=ft.Paint(color=ft.Colors.GREEN))
        )
        cp.shapes = state.shapes  # Обновляем список фигур
        cp.update()  # Обновляем холст

        # Обновляем текст с координатами
        coordinates_text.value = f"Координаты: ({x}, {y})"
        if len(state.shapes) > 1:
            coordinates = [(circle.x, circle.y) for circle in state.shapes]

            distance_px_value = abs(coordinates[0][0] - coordinates[1][0])

            print(coordinates)
            distance_cm_text.value = f"Дистанция 1 см = {distance_px_value} px"
        tab_content.update()

    # Изображение
    image = ft.Image(
        src="../video_dnerp/ball 240 2024-07-27 141246.png",
        # width=800,
        # height=600
    )

    # Холст для рисования точек
    cp = cv.Canvas(
        expand=True,
    )

    # Стек с изображением и холстом
    stack = ft.Stack([image, cp])

    # Оборачиваем весь `Stack` в `GestureDetector`
    gd = ft.GestureDetector(on_tap_up=mouse_test, content=stack)

    # Текст для координат
    coordinates_text = ft.Text("Координаты: (0, 0)")
    distance_cm_text = ft.Text("Дистанция 1 см = 0 px")

    def save_values(_):
        print('save', distance_px_value)

    save_button = ft.ElevatedButton(text="Сохранить значения ", on_click=save_values)

    tab_content = ft.Row(
        [
            ft.Column(
                [
                    coordinates_text,
                    distance_cm_text,
                    save_button
                ]
            ),
            gd,
        ]
    )
    return tab_content
