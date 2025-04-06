import base64
import os
import httpx
import asyncio
from io import BytesIO

import cv2
import flet as ft
from cvzone.ColorModule import ColorFinder

# Глобальная переменная для управления задачами
active_task = None
stop_event = asyncio.Event()


async def process_image(hsv_vals, image_path="images/golf_ball_50cm_240FPS_light.png"):
    """Обрабатывает изображение и возвращает цветовую маску."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл изображения не найден: {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")

    img = img[200:700, :]  # Обрезаем изображение
    color_finder = ColorFinder(False)
    img_color, _ = color_finder.update(img, hsv_vals)

    return img_color


async def opencv_task(hsv_vals, image_control):
    """Асинхронная задача для обновления изображения."""
    global stop_event
    stop_event.clear()  # Разрешаем выполнение цикла

    while not stop_event.is_set():
        img_color = await process_image(hsv_vals)

        # Преобразуем изображение в base64
        _, buffer = cv2.imencode('.jpg', img_color)
        img_bytes = BytesIO(buffer).getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Проверяем, что image_control добавлен на страницу
        #  Проверка image_control.page перед обновлением
        # → Если image_control удалён, opencv_task не вызовет ошибку.
        # когда переключаешь вкладки, создаётся новый image_control,
        # а opencv_task продолжает работать со старым элементом,
        # которого уже нет на странице. Это и вызывает ошибку
        if image_control.page is None:
            print("⚠️ Ошибка: image_control не добавлен на страницу, прерываем задачу.")
            return

        # Обновляем изображение в Flet
        image_control.src_base64 = img_base64
        image_control.update()

        await asyncio.sleep(0.05)  # Даем небольшую паузу, чтобы снизить нагрузку


async def load_hsv_tab():
    """Загружает вкладку HSV-настроек и управляет асинхронной задачей."""
    global active_task, stop_event

    hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 175, 'smax': 255, 'vmax': 255}

    def update_hsv(_):
        hsv_vals.update({
            'hmin': int(hmin.value),
            'smin': int(smin.value),
            'vmin': int(vmin.value),
            'hmax': int(hmax.value),
            'smax': int(smax.value),
            'vmax': int(vmax.value),
        })

        # Обновление текста значений
        hmin_text.value = f"Hue Min: {hsv_vals['hmin']}"
        smin_text.value = f"Saturation Min: {hsv_vals['smin']}"
        vmin_text.value = f"Value Min: {hsv_vals['vmin']}"
        hmax_text.value = f"Hue Max: {hsv_vals['hmax']}"
        smax_text.value = f"Saturation Max: {hsv_vals['smax']}"
        vmax_text.value = f"Value Max: {hsv_vals['vmax']}"

        tab_content.update()

    async def save_hsv_values(_):
        """Сохраняет HSV-значения и отправляет на сервер."""
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
    hmin, smin, vmin = [ft.Slider(min=0, max=255, value=hsv_vals[key], label=key, on_change=update_hsv) for key in
                        ['hmin', 'smin', 'vmin']]
    hmax, smax, vmax = [ft.Slider(min=0, max=255, value=hsv_vals[key], label=key, on_change=update_hsv) for key in
                        ['hmax', 'smax', 'vmax']]

    hmin_text, smin_text, vmin_text = [ft.Text(f"{key}: {hsv_vals[key]}") for key in ['hmin', 'smin', 'vmin']]
    hmax_text, smax_text, vmax_text = [ft.Text(f"{key}: {hsv_vals[key]}") for key in ['hmax', 'smax', 'vmax']]

    save_button = ft.ElevatedButton(text="Сохранить значения HSV", on_click=save_hsv_values)

    controls_column = ft.Column([
        ft.Text("Настройка параметров HSV:"),
        hmin, hmin_text,
        smin, smin_text,
        vmin, vmin_text,
        hmax, hmax_text,
        smax, smax_text,
        vmax, vmax_text,
        save_button,
    ])

    # Контроль для отображения изображения
    image_control = ft.Image(width=500, height=300, fit=ft.ImageFit.CONTAIN)

    tab_content = ft.Row([
        ft.Container(content=controls_column, bgcolor=ft.Colors.BROWN_600),
        ft.Container(content=image_control, bgcolor=ft.Colors.LIGHT_GREEN),
    ])

    # **ОСТАНАВЛИВАЕМ старую асинхронную задачу, если она уже работает**
    if active_task is not None:
        stop_event.set()  # Останавливаем цикл в `opencv_task`
        await active_task  # Ждем завершения задачи

    # **Запускаем новую асинхронную задачу**
    stop_event.clear()  # Разрешаем новый запуск
    active_task = asyncio.create_task(opencv_task(hsv_vals, image_control))

    return tab_content
