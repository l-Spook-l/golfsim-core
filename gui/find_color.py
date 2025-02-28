import base64
import os
import httpx
from io import BytesIO
from threading import Thread

import cv2
import flet as ft
from cvzone.ColorModule import ColorFinder


def process_image(hsv_vals, image_path="images/golf_ball_50cm_240FPS_light.png"):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл изображения не найден: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    # Загружаем изображение
    img = cv2.imread(image_path)
    img = img[200:700, :]  # Обрезка изображения

    # Создаем ColorFinder
    color_finder = ColorFinder(False)
    img_color, _ = color_finder.update(img, hsv_vals)
    return img_color


def opencv_thread(hsv_vals, image_control):
    while True:
        img_color = process_image(hsv_vals)

        # Преобразуем изображение в формат для Flet
        _, buffer = cv2.imencode('.jpg', img_color)
        img_bytes = BytesIO(buffer).getvalue()

        # Кодируем изображение в base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Обновляем картинку в Flet
        image_control.src_base64 = img_base64
        image_control.update()


def load_hsv_tab():
    # # Начальные значения HSV
    hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 175, 'smax': 255, 'vmax': 255}

    def update_hsv(_):
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

        tab_content.update()

    async def save_hsv_values(_):
        # Сохранение значений HSV и отправка на сервер
        print("Сохраненные значения HSV:", hsv_vals)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://192.168.50.107:8000/update-hsv",  # URL вашего сервера
                    json={"hsv_vals": hsv_vals}  # Данные для отправки
                )
                if response.status_code == 200:
                    print("Успешно отправлено на сервер:", response.json())
                else:
                    print("Ошибка при отправке на сервер:", response.text)
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")

    # Ползунки HSV
    hmin = ft.Slider(min=0, max=175, value=hsv_vals['hmin'], label="Hue Min", on_change=update_hsv)
    smin = ft.Slider(min=0, max=255, value=hsv_vals['smin'], label="Saturation Min", on_change=update_hsv)
    vmin = ft.Slider(min=0, max=255, value=hsv_vals['vmin'], label="Value Min", on_change=update_hsv)
    hmax = ft.Slider(min=0, max=175, value=hsv_vals['hmax'], label="Hue Max", on_change=update_hsv)
    smax = ft.Slider(min=0, max=255, value=hsv_vals['smax'], label="Saturation Max", on_change=update_hsv)
    vmax = ft.Slider(min=0, max=255, value=hsv_vals['vmax'], label="Value Max", on_change=update_hsv)

    # Тексты для отображения значений
    hmin_text = ft.Text(f"Hue Min: {hsv_vals['hmin']}")
    smin_text = ft.Text(f"Saturation Min: {hsv_vals['smin']}")
    vmin_text = ft.Text(f"Value Min: {hsv_vals['vmin']}")
    hmax_text = ft.Text(f"Hue Max: {hsv_vals['hmax']}")
    smax_text = ft.Text(f"Saturation Max: {hsv_vals['smax']}")
    vmax_text = ft.Text(f"Value Max: {hsv_vals['vmax']}")

    save_button = ft.ElevatedButton(text="Сохранить значения HSV", on_click=save_hsv_values)

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
            save_button,
        ]
    )

    # Контроль для отображения изображения
    image_control = ft.Image(width=500, height=300, fit=ft.ImageFit.CONTAIN)

    # Основной макет вкладки
    tab_content = ft.Row(
        [
            ft.Container(content=controls_column, bgcolor=ft.Colors.BROWN_600),
            ft.Container(content=image_control, bgcolor=ft.Colors.LIGHT_GREEN),
        ]
    )

    # Запуск OpenCV в отдельном потоке
    Thread(target=opencv_thread, args=(hsv_vals, image_control), daemon=True).start()

    return tab_content
