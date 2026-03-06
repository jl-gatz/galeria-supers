# main.py

import flet as ft
from application.use_cases import ListarSupers
from infrastructure.repositories.super_repository import SuperRepository
from ui.config.page_config import configurar_page

from galeria.ui.layout.root_layout import RootLayout
from galeria.ui.theme.theme import setup_theme
from galeria.ui.views.gallery_view import GalleryView


def main(page: ft.Page):
    setup_theme(page)
    configurar_page(page)

    repository = SuperRepository()
    use_case = ListarSupers(repository)  # type: ignore
    supers = use_case.executar()

    # Criamos a galeria primeiro
    gallery = GalleryView(supers, root_layout=None)  # type: ignore

    # Agora criamos o root passando a galeria
    root = RootLayout(gallery)

    # Injetamos root na galeria
    gallery.root = root

    page.add(root)


# Utilizando app ao invés de run, por conta da chamada para assets
ft.app(target=main, assets_dir="assets")  # type: ignore
