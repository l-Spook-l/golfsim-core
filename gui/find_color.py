import base64
import os
import asyncio
from io import BytesIO

import cv2
import flet as ft
from cvzone.ColorModule import ColorFinder

from data_base.config_db import async_session_maker
from data_base.db import DataBase
from data_base.models import HSVSetting
from exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError
from logging_config import logger


class FindBallByColor:
    def __init__(self):
        self.active_task = None
        self.stop_event = asyncio.Event()
        self.hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 255, 'smax': 255, 'vmax': 255}
        self.img_color = None
        self.image_control = ft.Image(width=1280, height=720, fit=ft.ImageFit.CONTAIN)
        self.controls_column = ft.Column()
        self.tab_content = ft.Row()
        self.error_text = ft.Text("", color=ft.Colors.RED, size=12, visible=False)

    async def get_active_hsv_profile(self):
        async with async_session_maker() as session:
            data = await DataBase.get_active_profile(session, HSVSetting)
            logger.info(f"Data active_hsv - {data.id}")

    async def save_hsv_values(self, hsv_value: dict, profile_name: str):
        # Получаем сессию
        logger.info('add_hsv_value -- hsv_value - ', hsv_value)
        mapping = {
            "hmin": "hue_min",
            "hmax": "hue_max",
            "smin": "saturation_min",
            "smax": "saturation_max",
            "vmin": "value_min",
            "vmax": "value_max",
        }
        mapped_data = {mapping[k]: v for k, v in hsv_value.items()}
        mapped_data['profile_name'] = profile_name
        # mapped_data['is_active'] = True

        try:
            async with async_session_maker() as session:
                success = await DataBase.save_hsv_or_pixel_value(session, HSVSetting, mapped_data)
                if success:
                    logger.info("Data added successfully")
                else:
                    logger.info("Failed to add data")
            self.error_text.visible = False
        except ProfileNameAlreadyExistsError:
            self.error_text.value = "A profile with this name already exists"
            self.error_text.visible = True
        except ProfileLimitReachedError:
            self.error_text.value = "You have reached the maximum number of profiles allowed"
            self.error_text.visible = True
        self.controls_column.update()

    async def process_image(self, hsv_vals):
        image_path = "folder_test_all_open/photo.jpg"
        """Обрабатывает изображение и возвращает цветовую маску."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл изображения не найден: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Не удалось загрузить изображение: {image_path}")

        # img = img[200:700, :]  # Обрезаем изображение
        color_finder = ColorFinder(False)
        self.img_color, _ = color_finder.update(img, hsv_vals)
        self.img_color = cv2.rotate(self.img_color, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self.img_color

    async def update_image_with_hsv(self, hsv_vals, image_control):
        """Асинхронная задача для обновления изображения."""
        self.stop_event.clear()  # Разрешаем выполнение цикла

        while not self.stop_event.is_set():
            img_color = await self.process_image(hsv_vals)

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
                logger.error("⚠️ Ошибка: image_control не добавлен на страницу, прерываем задачу.")
                return

            # Обновляем изображение в Flet
            image_control.src_base64 = img_base64
            image_control.update()

            await asyncio.sleep(0.05)  # Даем небольшую паузу, чтобы снизить нагрузку

    async def load_hsv_tab(self):
        """Загружает вкладку HSV-настроек и управляет асинхронной задачей."""

        def update_hsv(_):
            self.hsv_vals.update({
                'hmin': int(hmin.value),
                'smin': int(smin.value),
                'vmin': int(vmin.value),
                'hmax': int(hmax.value),
                'smax': int(smax.value),
                'vmax': int(vmax.value),
            })

            # Обновление текста значений
            hmin_text.value = f"Hue Min: {self.hsv_vals['hmin']}"
            smin_text.value = f"Saturation Min: {self.hsv_vals['smin']}"
            vmin_text.value = f"Value Min: {self.hsv_vals['vmin']}"
            hmax_text.value = f"Hue Max: {self.hsv_vals['hmax']}"
            smax_text.value = f"Saturation Max: {self.hsv_vals['smax']}"
            vmax_text.value = f"Value Max: {self.hsv_vals['vmax']}"

            self.tab_content.update()

        # Ползунки HSV
        hmin, smin, vmin = [ft.Slider(min=0, max=255, value=self.hsv_vals[key], label=key, on_change=update_hsv) for key in
                            ['hmin', 'smin', 'vmin']]
        hmax, smax, vmax = [ft.Slider(min=0, max=255, value=self.hsv_vals[key], label=key, on_change=update_hsv) for key in
                            ['hmax', 'smax', 'vmax']]

        # hmin_text, smin_text, vmin_text = [ft.Text(f"{key}: {hsv_vals[key]}") for key in ['hmin', 'smin', 'vmin']]
        # hmax_text, smax_text, vmax_text = [ft.Text(f"{key}: {hsv_vals[key]}") for key in ['hmax', 'smax', 'vmax']]
        hmin_text = ft.Text(f"Hue Min: {self.hsv_vals['hmin']}")
        smin_text = ft.Text(f"Saturation Min: {self.hsv_vals['smin']}")
        vmin_text = ft.Text(f"Value Min: {self.hsv_vals['vmin']}")
        hmax_text = ft.Text(f"Hue Max: {self.hsv_vals['hmax']}")
        smax_text = ft.Text(f"Saturation Max: {self.hsv_vals['smax']}")
        vmax_text = ft.Text(f"Value Max: {self.hsv_vals['vmax']}")

        active_profile_info = ft.Container(
            content=await self.get_active_hsv_profile(),
            bgcolor=ft.Colors.YELLOW_800,
            height=100,
            width=500
        )

        async def handle_save_button_click(e):
            await self.save_hsv_values(self.hsv_vals, profile_name_field.value)

        profile_name_field = ft.TextField(label="Profile name", width=200)
        save_profile_button = ft.ElevatedButton(
            text="Сохранить значения HSV",
            on_click=handle_save_button_click  # e - необходимо для работы
        )

        controls_column = ft.Column([
            profile_name_field,
            self.error_text,
            ft.Text("Настройка параметров HSV:"),
            hmin, hmin_text,
            smin, smin_text,
            vmin, vmin_text,
            hmax, hmax_text,
            smax, smax_text,
            vmax, vmax_text,
            save_profile_button,
        ])

        # Контроль для отображения изображения
        # self.image_control = ft.Image(width=1280, height=720, fit=ft.ImageFit.CONTAIN)

        self.tab_content = ft.Row([
            # active_profile_info,
            ft.Container(content=self.controls_column, bgcolor=ft.Colors.GREEN_400, padding=10),
            ft.Container(content=self.image_control, bgcolor=ft.Colors.GREY_400),
        ])

        # **ОСТАНАВЛИВАЕМ старую асинхронную задачу, если она уже работает**
        if self.active_task is not None:
            self.stop_event.set()  # Останавливаем цикл в `opencv_task`
            try:
                await self.active_task  # Дожидаемся завершения задачи
            except asyncio.CancelledError:
                logger.info("Предыдущая задача OpenCV успешно остановлена.")

        # **Запускаем новую асинхронную задачу**
        self.stop_event.clear()  # Разрешаем новый запуск
        self.active_task = asyncio.create_task(self.update_image_with_hsv(self.hsv_vals, self.image_control))

        return self.tab_content
