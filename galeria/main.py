# main.py

import flet as ft
from application.use_cases import ListarSupers
from infrastructure.repositories.super_repository import SuperRepository
from ui.components.gallery_view import GalleryView
from ui.config.page_config import configurar_page

from galeria.ui.layout.root_layout import RootLayout


def main(page: ft.Page):
    configurar_page(page)

    repository = SuperRepository()
    use_case = ListarSupers(repository)
    supers = use_case.executar()

    # navigator = Navigator(page)

    # Criamos a galeria primeiro
    gallery = GalleryView(supers, root_layout=None)

    # Agora criamos o root passando a galeria
    root = RootLayout(gallery)

    # Injetamos root na galeria
    gallery.root = root

    page.add(root)


ft.app(target=main, assets_dir="assets")
