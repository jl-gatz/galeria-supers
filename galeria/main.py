# main.py

import flet as ft
from application.use_cases import ListarSupers
from infrastructure.repositories.super_repository import SuperRepository
from ui.components.gallery_view import GalleryView
from ui.config.page_config import configurar_page
from ui.navigation.navigator import Navigator


def main(page: ft.Page):
    configurar_page(page)

    repository = SuperRepository()
    use_case = ListarSupers(repository)
    supers = use_case.executar()

    navigator = Navigator(page)

    home = GalleryView(supers, navigator)
    navigator.go(home)


ft.app(target=main, assets_dir="assets")
