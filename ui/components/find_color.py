import base64
import os
import asyncio
import shutil
from io import BytesIO

import cv2
import flet as ft
from cvzone.ColorModule import ColorFinder
from numpy import ndarray

from states.app_page_state import PageState
from data_base.config_db import async_session_maker
from data_base.repositories.hsv_setting import HSVSettingRepository
from core.exceptions import ProfileNameAlreadyExistsError, ProfileLimitReachedError
from core.logging_config import logger


class FindBallByColor:
    """
    Class for detecting the ball by color using HSV settings.

    Main functionality:
    - Processes the uploaded image and creates a color mask using HSV.
    - Asynchronously updates the image on the Flet page.
    - Configures and saves HSV profiles for different colors.
    - Manages the asynchronous OpenCV task for updating the image.

    Attributes:
        page (PageState): Flet page object.
        active_task (asyncio.Task | None): Current async image update task.
        stop_event (asyncio.Event): Event to stop the async task.
        hsv_vals (dict): Dictionary with current HSV parameters.
        image_path (str): Path to the uploaded image.
        image_src (str): Path or base64 string of the current image.
        img_color (numpy.ndarray | None): Image with applied color mask.
        image_control (ft.Image): UI element for displaying the image.
        controls_column (ft.Column): Container with HSV control elements.
        tab_content (ft.Row): Tab container with HSV settings and image.
    """

    def __init__(self):
        self.page = PageState.get_page()
        self.active_task = None
        self.stop_event = asyncio.Event()
        self.hsv_vals: dict = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 255, 'smax': 255, 'vmax': 255}
        self.image_path: str = "mobile_uploads/images/photo.jpg"
        self.image_src: str = ""
        self.img_color = None
        self.image_control = ft.Image(width=1280, height=720, fit=ft.ImageFit.CONTAIN)
        self.controls_column = ft.Column()
        self.tab_content = ft.Row()

    def show_snackbar(self, message: str, status: str) -> None:
        """
        Displays a notification on the Flet page.

        Args:
            message (str): Message text.
            status (str): Notification status ("success" or "error").
        """
        self.page.open(
            ft.SnackBar(
                ft.Text(f"{message}"),
                bgcolor=ft.Colors.GREEN_ACCENT_700 if status == "success" else ft.Colors.RED_ACCENT_700
            )
        )
        self.page.update()

    async def save_hsv_values(self, hsv_value: dict, profile_name: str) -> None:
        """
        Saves HSV settings as a profile.

        Args:
            hsv_value (dict): Dictionary with HSV parameters.
            profile_name (str): Name of the profile.

        Raises:
            ProfileNameAlreadyExistsError: If a profile with this name already exists.
            ProfileLimitReachedError: If the profile limit has been reached.
        """
        if len(profile_name) < 2:
            self.show_snackbar("Profile name too short", "error")
            return None
        logger.info('add_hsv_value -- hsv_value - ', hsv_value)
        new_folder = "mobile_uploads/images/profile_images/"
        new_name = f"{profile_name.replace(' ', '-')}.jpg".lower()
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
        mapped_data["photo"] = f"{new_folder}{new_name}"

        try:
            async with async_session_maker() as session:
                repo = HSVSettingRepository(session)
                success = await repo.add_new_hsv_set(mapped_data)
                if success:
                    logger.info("Data added successfully")
                    self.show_snackbar("HSV settings have been successfully saved", "success")
                    shutil.copy(self.image_path, mapped_data["photo"])
                else:
                    logger.info("Failed to add data")
                    self.show_snackbar("Failed to add data", "error")
        except ProfileNameAlreadyExistsError:
            self.show_snackbar("A profile with this name already exists", "error")
        except ProfileLimitReachedError:
            self.show_snackbar("You have reached the maximum number of profiles allowed", "error")
        self.controls_column.update()

    async def process_image(self, hsv_vals: dict) -> ndarray:
        """
        Processes the image and returns a color mask.

        Args:
            hsv_vals (dict): Dictionary with HSV parameters.

        Returns:
            numpy.ndarray: Image with the color highlighted.

        Raises:
            FileNotFoundError: If the image file is not found.
            ValueError: If the image could not be loaded.
        """
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Image file not found: {self.image_path}")

        img = cv2.imread(self.image_path)
        if img is None:
            raise ValueError(f"Failed to load image: {self.image_path}")

        color_finder = ColorFinder(False)
        self.img_color, _ = color_finder.update(img, hsv_vals)
        self.img_color = cv2.rotate(self.img_color, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self.img_color

    async def update_image_with_hsv(self, hsv_vals: dict, image_control: ft.Image) -> None:
        """
        Asynchronous task for updating the image with the applied HSV mask.

        Args:
            hsv_vals (dict): Current HSV settings.
            image_control (ft.Image): Flet element for updating the image.
        """
        self.stop_event.clear()  # Allow loop execution

        while not self.stop_event.is_set():
            img_color = await self.process_image(hsv_vals)

            # Convert the image to base64
            _, buffer = cv2.imencode('.jpg', img_color)
            img_bytes = BytesIO(buffer).getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

            # Check that image_control is added to the page
            # Check image_control.page before updating
            # → If image_control is removed, opencv_task won't throw an error.
            # When switching tabs, a new image_control is created,
            # but opencv_task continues working with the old element,
            # which is no longer on the page. This causes the error.
            if image_control.page is None:
                logger.error("Error: image_control was not added to the page. Aborting the task")
                return

            # Update the image in Flet
            image_control.src_base64 = img_base64
            image_control.update()
            # Add a short pause to reduce the load
            await asyncio.sleep(0.05)

    async def build_section(self) -> ft.Row:
        """
        Creates the tab interface for HSV settings and starts the asynchronous OpenCV task.

        Returns:
            ft.Row: Tab container with controls and image.
        """

        def update_hsv(_):
            self.hsv_vals.update({
                'hmin': int(hmin.value),
                'smin': int(smin.value),
                'vmin': int(vmin.value),
                'hmax': int(hmax.value),
                'smax': int(smax.value),
                'vmax': int(vmax.value),
            })

            # Update the text values
            hmin_text.value = f"Hue Min: {self.hsv_vals['hmin']}"
            smin_text.value = f"Saturation Min: {self.hsv_vals['smin']}"
            vmin_text.value = f"Value Min: {self.hsv_vals['vmin']}"
            hmax_text.value = f"Hue Max: {self.hsv_vals['hmax']}"
            smax_text.value = f"Saturation Max: {self.hsv_vals['smax']}"
            vmax_text.value = f"Value Max: {self.hsv_vals['vmax']}"

            self.tab_content.update()

        # HSV sliders
        hmin, smin, vmin = [ft.Slider(min=0, max=255, value=self.hsv_vals[key],
                                      label=key,
                                      on_change=update_hsv,
                                      inactive_color=ft.Colors.GREY)
                            for key in ['hmin', 'smin', 'vmin']]
        hmax, smax, vmax = [ft.Slider(min=0, max=255, value=self.hsv_vals[key],
                                      label=key,
                                      on_change=update_hsv,
                                      inactive_color=ft.Colors.GREY)
                            for key in ['hmax', 'smax', 'vmax']]

        hmin_text = ft.Text(f"Hue Min: {self.hsv_vals['hmin']}")
        smin_text = ft.Text(f"Saturation Min: {self.hsv_vals['smin']}")
        vmin_text = ft.Text(f"Value Min: {self.hsv_vals['vmin']}")
        hmax_text = ft.Text(f"Hue Max: {self.hsv_vals['hmax']}")
        smax_text = ft.Text(f"Saturation Max: {self.hsv_vals['smax']}")
        vmax_text = ft.Text(f"Value Max: {self.hsv_vals['vmax']}")

        profile_name_field = ft.TextField(
            label="Profile name",
            width=200,
            max_length=20,
        )

        async def handle_save_button_click(e):
            await self.save_hsv_values(self.hsv_vals, profile_name_field.value)

        save_profile_button = ft.ElevatedButton(
            text="Save HSV values",
            on_click=handle_save_button_click
        )

        self.controls_column = ft.Column([
            profile_name_field,
            ft.Text("HSV parameter settings:"),
            hmin_text, hmin,
            smin_text, smin,
            vmin_text, vmin,
            hmax_text, hmax,
            smax_text, smax,
            vmax_text, vmax,
            save_profile_button,
        ])

        self.tab_content = ft.Row([
            ft.Container(content=self.controls_column, bgcolor="#E4E7EB", padding=10, margin=5, border_radius=10),
            ft.Container(content=self.image_control, bgcolor="#E4E7EB", padding=10, border_radius=10),
        ])

        # STOP the old asynchronous task if it is already running
        if self.active_task is not None:
            self.stop_event.set()  # Stop the loop in `opencv_task`
            try:
                await self.active_task  # Wait for the task to finish
            except asyncio.CancelledError:
                logger.info("The previous OpenCV process has been successfully stopped")

        # Start a new asynchronous task
        self.stop_event.clear()  # Allow new start
        self.active_task = asyncio.create_task(self.update_image_with_hsv(self.hsv_vals, self.image_control))

        return self.tab_content
