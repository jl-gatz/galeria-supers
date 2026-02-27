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
