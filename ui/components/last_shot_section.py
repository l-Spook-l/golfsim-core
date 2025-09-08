import flet as ft

from states.shot_state import ShotState, AngleType
from states.app_page_state import PageState
from data_base.schemas import LastGolfShotSchema
from ui.components.drive_range_dashboard import DriveRangeDashboard


class LastShotSection:
    """
    Class for displaying and managing the "Last Shot" section.

    Main functionality:
    - Displays information about the last shot.
    - Allows selection and switching of the active club.
    - Switches between angle analysis mode (vertical/horizontal).
    - Forms a UI block with a table of shot parameters and a dashboard.

    Attributes:
        page (PageState): the current Flet page object.
        last_shot (dict): data about the last shot (corresponds to LastGolfShotSchema).
        active_club (dict): the currently selected club {"name": str, "image": str}.
        angle_mode (str | None): the angle analysis mode (vertical/horizontal).
        golf_clubs (dict): dictionary of available clubs.
        dlg_modal (ft.AlertDialog): dialog window for club selection.
        button_select_club (ft.Container | None): button for selecting a club.
        shot_state (ShotState): the shot state object.
        drive_range_dashboard (DriveRangeDashboard): the training field dashboard.
    """

    def __init__(self, last_shot: dict):
        """
        Args:
            last_shot (dict): data about the last shot.
        """
        self.page = PageState.get_page()
        self.last_shot = last_shot
        self.active_club = {"name": "", "image": ""}
        self.angle_mode = None
        self.golf_clubs = {}
        self.dlg_modal = ft.AlertDialog()
        self.button_select_club = None
        self.shot_state = ShotState()
        self.drive_range_dashboard = DriveRangeDashboard()

    async def load_clubs_info(self):
        """
        Loads information about the clubs from the shot state.

        Sets the active club and the dictionary of available clubs.
        """
        self.golf_clubs = self.shot_state.golf_clubs
        name_active_club = self.shot_state.club
        self.active_club = {
            "name": name_active_club,
            "image": self.golf_clubs.get(name_active_club).get("image")
        }

    def update_selected_club(self, club_name: str, club_image_src: str):
        """
        Updates the selected club and saves it to the state.

        Args:
            club_name (str): name of the club.
            club_image_src (str): path to the image of the club.
        """
        self.active_club["name"] = club_name
        self.active_club["image"] = club_image_src

        self.button_select_club.content = ft.Column([
            ft.Text(club_name, size=32, text_align=ft.TextAlign.CENTER),
            ft.Image(src=club_image_src, width=110, height=100),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.shot_state.club = club_name
        self.shot_state.save()
        self.page.close(self.dlg_modal)
        self.page.update()

    def build_club_selector(self) -> ft.AlertDialog:
        """
        Creates a dialog window for selecting a club.

        Returns:
            ft.AlertDialog: a window for selecting clubs.
        """
        return ft.AlertDialog(
            title=ft.Text("Choose a club", size=25, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            width=160,
                            height=130,
                            bgcolor="#FFFFFF",
                            border=ft.border.all(1, "#CCCCCC"),
                            border_radius=20,
                            padding=10,
                            margin=5,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                [
                                    ft.Text(f"{club[0]}", size=18),
                                    ft.Image(src=club[1].get("image"), width=75, height=75, fit=ft.ImageFit.CONTAIN),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ink=True,
                            on_click=lambda e, club_name=club[0], club_image_src=club[1].get("image"):
                            self.update_selected_club(club_name, club_image_src)
                        )
                        for club in list(self.golf_clubs.items())[i:i + 4]
                    ])
                    for i in range(0, len(self.golf_clubs), 4)
                ], spacing=10),
                height=400,
            ),
            bgcolor="#E4E7EB",
        )

    def set_angle_mode(self):
        """
        Creates a component for switching the angle analysis mode.

        Returns:
            ft.Container: a container with a switch (RadioGroup).
        """
        mode_txt = ft.Text("Angle mode", size=24)

        def set_mode(val: str):
            match val:
                case "vertical":
                    self.shot_state.angle_type = AngleType.VERTICAL
                    pass
                case "horizontal":
                    self.shot_state.angle_type = AngleType.HORIZONTAL
                    pass
                # TODO реализация одновременного анализа двух углов
                # case "both":
                #     pass

        rg = ft.RadioGroup(
            value=self.shot_state.angle_type.value,
            on_change=lambda e: set_mode(e.control.value),
            content=ft.Column([
                ft.Radio(value="vertical", label="Vertical", label_style=ft.TextStyle(size=18)),
                ft.Radio(value="horizontal", label="Horizontal", label_style=ft.TextStyle(size=18)),
            ])
        )
        return ft.Container(
            content=ft.Column([
                mode_txt,
                rg
            ]),
            bgcolor="#E8F5E9",
            border=ft.border.all(1, "black"),
            border_radius=10,
            alignment=ft.alignment.center,
            width=180,
            padding=10
        )

    def build_last_shot_table(self) -> ft.Container:
        """
        Generates a data table for the last shot with options for selecting the club and angle mode.

        Returns:
            ft.Container: a container with the table and control buttons.
        """
        last_shot_data = []
        for field_name, field_value in LastGolfShotSchema.model_fields.items():
            title = field_value.title
            value = self.last_shot.get(field_name)
            row = ft.Container(
                content=ft.Column([
                    ft.Text(title, size=35, width=180, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"{value}", size=45, width=180, text_align=ft.TextAlign.CENTER),
                ]),
                bgcolor="#E8F5E9",
                border=ft.border.all(1, "black"),
                border_radius=10,
                alignment=ft.alignment.center,
                width=280,
            )
            last_shot_data.append(row)

        self.button_select_club = ft.Container(
            width=180,
            bgcolor="#E8F5E9",
            border=ft.border.all(1, "black"),
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Text(self.active_club.get("name"), size=32, text_align=ft.TextAlign.CENTER),
                ft.Image(src=self.active_club.get("image"), width=110, height=110),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ink=True,
            on_click=lambda e: self.page.open(self.dlg_modal)
        )

        last_shot_data.append(self.button_select_club)
        last_shot_data.append(self.set_angle_mode())

        return ft.Container(
            content=ft.Row(
                controls=last_shot_data,
                spacing=10
            ),
            bgcolor="#C8E6C9",
            padding=10,
            border_radius=15,
            height=180
        )

    async def build_section(self) -> ft.Container:
        """
        Assembles the "Last Shot" section:
        - loads club data
        - initializes the club selection dialog
        - creates the last shot data table
        - connects the dashboard

        Returns:
            ft.Container: the ready UI block to be inserted into the app.
        """
        await self.load_clubs_info()
        self.dlg_modal = self.build_club_selector()
        last_shot_table = self.build_last_shot_table()
        load_drive_range_dashboard = DriveRangeDashboard()
        self.drive_range_dashboard = await load_drive_range_dashboard.build_section()

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=last_shot_table,
                ),
            ]),
        )
