# galeria/ui/theme/theme.py
"""Aplicação direta de tema na página Flet."""

import flet as ft

from galeria.ui.theme.manager import ThemeManager

from .models import Theme


def setup_theme(page: ft.Page, theme_manager: ThemeManager):
    """Registra fontes e sincroniza a página com o tema ativo."""
    page.fonts = {
        "Montserrat": "fonts/Montserrat-Regular.ttf",
        "Montserrat-Bold": "fonts/Montserrat-Bold.ttf",
    }

    def apply_theme(theme: Theme):
        """Aplica título e fundo sempre que o tema muda."""
        page.title = theme.title
        page.bgcolor = theme.base.background

        if page.session:  # evita update prematuro
            page.update()

    # 🔗 registra listener
    theme_manager.subscribe(apply_theme)

    # 🚀 aplica tema inicial via mesmo caminho
    apply_theme(theme_manager.theme)
