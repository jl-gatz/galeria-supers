# main.py


import flet as ft
from infrastructure.repositories.super_repository import SuperRepository
from ui.config.page_config import configurar_page

from galeria.core import ASSETS_URL
from galeria.domain import SuperService
from galeria.ui.layout import RootLayout
from galeria.ui.theme import setup_theme
from galeria.ui.views import GalleryView


def main(page: ft.Page):
    setup_theme(page)
    configurar_page(page)

    repository = SuperRepository()
    service = SuperService(repository=repository)

    # Criamos a galeria primeiro
    gallery = GalleryView(service=service, page=page, root_layout=None)  # type: ignore

    # Agora criamos o root passando a galeria
    root = RootLayout(gallery)

    # Injetamos root na galeria
    gallery.root = root

    page.add(root)

    page.scroll = ft.ScrollMode.HIDDEN


# Utilizando app ao invés de run, por conta da chamada para assets
ft.app(target=main, assets_dir=str(ASSETS_URL))  # type: ignore
