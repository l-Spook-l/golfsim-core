import flet as ft


class PageState:
    """
    A singleton-like class to store and provide global access to the Flet page instance.
    Ensures only one page is initialized during the app lifecycle.
    """
    __page: ft.Page = None

    @classmethod
    def set_page(cls, page: ft.Page) -> None:
        """
        Sets the page instance if it hasn't been set already.

        Args:
            page (ft.Page): The Flet page instance.

        Raises:
            ValueError: If the page has already been set.
        """
        if cls.__page is not None:
            raise ValueError("❌ The page has already been initialized! It's not possible to create multiple pages.")
        cls.__page = page

    @classmethod
    def get_page(cls) -> ft.Page:
        """
        Retrieves the current page instance.

        Returns:
            ft.Page: The Flet page instance.

        Raises:
            ValueError: If the page has not been initialized.
        """
        if cls.__page is None:
            raise ValueError("❌ The page has not been initialized.")
        return cls.__page
