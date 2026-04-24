import flet as ft

from galeria.ui.theme.manager import ThemeManager

from .models import Theme


def setup_theme(page: ft.Page, theme_manager: ThemeManager):
    theme = theme_manager.theme

    page.title = theme.title
    page.bgcolor = theme.background

    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
    }

    def update_page(theme: Theme):
        page.title = theme.title
        page.bgcolor = theme.background
        page.update()

    theme_manager.subscribe(update_page)
