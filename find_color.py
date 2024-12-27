import base64
import cv2
import flet as ft
from threading import Thread
from cvzone.ColorModule import ColorFinder
from io import BytesIO


def process_image(hsv_vals, image_path="images/golf_ball_50cm_240FPS_light.png"):
    # Загружаем изображение
    img = cv2.imread(image_path)
    img = img[200:700, :]  # Обрезка изображения

    # Создаем ColorFinder
    color_finder = ColorFinder(False)
    img_color, _ = color_finder.update(img, hsv_vals)
    return img_color


def opencv_thread(page, hsv_vals, image_control):
    while True:
        img_color = process_image(hsv_vals)

        # Преобразуем изображение в формат для Flet
        _, buffer = cv2.imencode('.jpg', img_color)
        img_bytes = BytesIO(buffer).getvalue()

        # Кодируем изображение в base64 с использованием стандартной библиотеки base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Обновляем картинку в Flet
        image_control.src_base64 = img_base64
        page.update()


def find_main(page: ft.Page):
    # Начальные значения HSV
    hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 175, 'smax': 255, 'vmax': 255}

    def update_hsv(e):
        # Обновление значений HSV
        hsv_vals['hmin'] = int(hmin.value)
        hsv_vals['smin'] = int(smin.value)
        hsv_vals['vmin'] = int(vmin.value)
        hsv_vals['hmax'] = int(hmax.value)
        hsv_vals['smax'] = int(smax.value)
        hsv_vals['vmax'] = int(vmax.value)

        # Обновление текста значений
        hmin_text.value = f"Hue Min: {hsv_vals['hmin']}"
        smin_text.value = f"Saturation Min: {hsv_vals['smin']}"
        vmin_text.value = f"Value Min: {hsv_vals['vmin']}"
        hmax_text.value = f"Hue Max: {hsv_vals['hmax']}"
        smax_text.value = f"Saturation Max: {hsv_vals['smax']}"
        vmax_text.value = f"Value Max: {hsv_vals['vmax']}"

        page.update()

    # Ползунки HSV
    hmin = ft.Slider(min=0, max=179, value=hsv_vals['hmin'], label="Hue Min", on_change=update_hsv)
    smin = ft.Slider(min=0, max=255, value=hsv_vals['smin'], label="Saturation Min", on_change=update_hsv)
    vmin = ft.Slider(min=0, max=255, value=hsv_vals['vmin'], label="Value Min", on_change=update_hsv)
    hmax = ft.Slider(min=0, max=179, value=hsv_vals['hmax'], label="Hue Max", on_change=update_hsv)
    smax = ft.Slider(min=0, max=255, value=hsv_vals['smax'], label="Saturation Max", on_change=update_hsv)
    vmax = ft.Slider(min=0, max=255, value=hsv_vals['vmax'], label="Value Max", on_change=update_hsv)

    # Тексты для отображения значений
    hmin_text = ft.Text(f"Hue Min: {hsv_vals['hmin']}")
    smin_text = ft.Text(f"Saturation Min: {hsv_vals['smin']}")
    vmin_text = ft.Text(f"Value Min: {hsv_vals['vmin']}")
    hmax_text = ft.Text(f"Hue Max: {hsv_vals['hmax']}")
    smax_text = ft.Text(f"Saturation Max: {hsv_vals['smax']}")
    vmax_text = ft.Text(f"Value Max: {hsv_vals['vmax']}")

    # Контейнер с ползунками и значениями
    controls_column = ft.Column(
        [
            ft.Text("Настройка параметров HSV:"),
            hmin,
            hmin_text,
            smin,
            smin_text,
            vmin,
            vmin_text,
            hmax,
            hmax_text,
            smax,
            smax_text,
            vmax,
            vmax_text,
        ]
    )

    # Контроль для отображения изображения
    image_control = ft.Image(width=500, height=300, fit=ft.ImageFit.CONTAIN)

    # Основной макет: две части (ползунки и изображение)
    page.add(
        ft.Row(
            [
                ft.Container(content=controls_column, expand=1),
                ft.Container(content=image_control, expand=1),
            ]
        )
    )

    # Запуск OpenCV в отдельном потоке
    Thread(target=opencv_thread, args=(page, hsv_vals, image_control), daemon=True).start()


if __name__ == "__main__":
    ft.app(target=find_main)

