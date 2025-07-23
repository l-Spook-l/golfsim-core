import flet as ft


class AppContext:
    __page: ft.Page = None

    @classmethod
    def set_page(cls, page: ft.Page):
        """Sets the page only if it hasn't been set already."""
        if cls.__page is not None:
            raise ValueError("❌ The page has already been initialized! It's not possible to create multiple pages.")
        cls.__page = page

    @classmethod
    def get_page(cls) -> ft.Page:
        """Returns the current page. Raises an error if the page has not been set."""
        if cls.__page is None:
            raise ValueError("❌ The page has not been initialized.")
        return cls.__page
