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
        "Lora-BoldItalic": "fonts/Lora-BoldItalic.ttf",
        "Lora-Bold": "fonts/Lora-Bold.ttf",
        "Lora-Italic": "fonts/Lora-Italic.ttf",
        "Lora-MediumItalic": "fonts/Lora-MediumItalic.ttf",
        "Lora-Medium": "fonts/Lora-Medium.ttf",
        "Lora-Regular": "fonts/Lora-Regular.ttf",
        "Lora-SemiBold": "fonts/Lora-SemiBold.ttf",
        "Lora-SemiBoldItalic": "fonts/Lora-SemiBoldItalic.ttf",
        "Manrope-Bold": "fonts/Manrope-Bold.ttf",
        "Manrope-ExtraBold": "fonts/Manrope-ExtraBold.ttf",
        "Manrope-ExtraLight": "fonts/Manrope-ExtraLight.ttf",
        "Manrope-Light": "fonts/Manrope-Light.ttf",
        "Manrope-Medium": "fonts/Manrope-Medium.ttf",
        "Manrope-Regular": "fonts/Manrope-Regular.ttf",
        "Manrope-SemiBold": "fonts/Manrope-SemiBold.ttf",
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
        "SourceSans3-BlackItalic": "fonts/SourceSans3-BlackItalic.ttf",
        "SourceSans3-Black": "fonts/SourceSans3-Black.ttf",
        "SourceSans3-BoldItalic": "fonts/SourceSans3-BoldItalic.ttf",
        "SourceSans3-Bold": "fonts/SourceSans3-Bold.ttf",
        "SourceSans3-ExtraBoldItalic": "fonts/SourceSans3-ExtraBoldItalic.ttf",
        "SourceSans3-ExtraBold": "fonts/SourceSans3-ExtraBold.ttf",
        "SourceSans3-ExtraLightItalic": "fonts/SourceSans3-ExtraLightItalic.ttf",
        "SourceSans3-ExtraLight": "fonts/SourceSans3-ExtraLight.ttf",
        "SourceSans3-Italic": "fonts/SourceSans3-Italic.ttf",
        "SourceSans3-LightItalic": "fonts/SourceSans3-LightItalic.ttf",
        "SourceSans3-Light": "fonts/SourceSans3-Light.ttf",
        "SourceSans3-MediumItalic": "fonts/SourceSans3-MediumItalic.ttf",
        "SourceSans3-Medium": "fonts/SourceSans3-Medium.ttf",
        "SourceSans3-Regular": "fonts/SourceSans3-Regular.ttf",
        "SourceSans3-SemiBoldItalic": "fonts/SourceSans3-SemiBoldItalic.ttf",
        "SourceSans3-SemiBold": "fonts/SourceSans3-SemiBold.ttf",
    }
