import flet as ft

from galeria.ui.theme.manager import ThemeManager

from .models import Theme


def setup_theme(page: ft.Page, theme_manager: ThemeManager):
    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
    }

    def apply_theme(theme: Theme):
        page.title = theme.title
        page.bgcolor = theme.background

        if page.session:  # evita update prematuro
            page.update()

    # 🔗 registra listener
    theme_manager.subscribe(apply_theme)

    # 🚀 aplica tema inicial via mesmo caminho
    apply_theme(theme_manager.theme)
