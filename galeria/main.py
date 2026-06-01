# galeria/main.py
"""Ponto de entrada da aplicação Flet."""

import flet as ft

from galeria.core import ASSETS_URL
from galeria.domain import SuperService
from galeria.infrastructure.repositories.super_repository import SuperRepository
from galeria.ui.config.page_config import configurar_page
from galeria.ui.layout import RootLayout
from galeria.ui.theme.manager import ThemeManager
from galeria.ui.theme.themes import CCUEC_THEME
from galeria.ui.views import GalleryView


def main(page: ft.Page) -> None:
    """Configura dependências, tema e layout raiz da aplicação."""
    configurar_page(page)

    repository = SuperRepository()
    service = SuperService(repository=repository)

    # Tema padrão da galeria (pode ser alterado dinamicamente depois)
    theme = ThemeManager(CCUEC_THEME)
    # Criamos a galeria primeiro
    gallery = GalleryView(
        service=service, page=page, root_layout=None, theme=theme
    )  # root_layout será injetado depois

    # Agora criamos o root passando a galeria
    root = RootLayout(gallery, theme_manager=theme)

    # Injetamos root na galeria
    gallery.root = root

    # Configuramos o page para mostrar o root
    page.add(
        ft.Column(
            expand=True,
            controls=[root],
        )
    )

    page.scroll = ft.ScrollMode.HIDDEN


if __name__ == "__main__":
    # Utilizando app ao invés de run, por conta da chamada para assets
    ft.app(target=main, assets_dir=str(ASSETS_URL))  # type: ignore
