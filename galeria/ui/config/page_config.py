# config/page_config.py

import flet as ft
from core.config import APP_TITLE


def configurar_page(page: ft.Page) -> None:
    """
    Configurações gerais da janela do app
    """
    page.title = APP_TITLE
    page.window.full_screen = True
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    page.window.frameless = True

    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Light": "fonts/Montserrat-Light.ttf",
        "Montserrat-Light-Italic": "fonts/Montserrat-LightItalic.ttf",
        "Montserrat-Medium": "fonts/Montserrat-Medium.ttf",
        "Montserrat-Medium-Italic": "fonts/Montserrat-MediumItalic.ttf",
        "Montserrat-Italic": "fonts/Montserrat-Italic.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
        "Montserrat-Bold-Italic": "fonts/Montserrat-BoldItalic.ttf",
        "Montserrat-EXTRA": "fonts/Montserrat-Extrabold.ttf",
        "Montserrat-EXTRA-Italic": "fonts/Montserrat-ExtraboldItalic.ttf",
        "Montserrat-EXTRA-Light": "fonts/Montserrat-ExtraLight.ttf",
        "Montserrat-BLACK": "fonts/Montserrat-Black.ttf",
        "Montserrat-BLACK-Italic": "fonts/Montserrat-BlackItalice.ttf",
        "Montserrat-Regular": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Semi-Bold": "fonts/Montserrat-SemiBold.ttf",
        "Montserrat-Semi-Bold-Italic": "fonts/Montserrat-SemiBoldItalic.ttf",
        "Montserrat-Thin": "fonts/Montserrat-Thin.ttf",
        "Montserrat-Thin-Italic": "fonts/Montserrat-ThinItalic.ttf",
    }
