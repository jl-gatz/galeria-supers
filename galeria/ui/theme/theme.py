import flet as ft

from galeria.ui.theme import BACKGROUND


def setup_theme(page: ft.Page):
    page.title = "Galeria de Superintendentes"
    page.bgcolor = BACKGROUND

    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
    }
