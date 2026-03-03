import flet as ft


def setup_theme(page: ft.Page):
    page.title = "Galeria de Superintendentes"
    page.bgcolor = "#F4F4F4"

    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
    }
