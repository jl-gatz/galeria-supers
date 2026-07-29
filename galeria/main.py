# galeria/main.py
"""Ponto de entrada da aplicação Flet."""

from collections.abc import Awaitable, Callable
from typing import Protocol, cast

import flet as ft

from galeria.core.paths import ASSETS_DIR
from galeria.domain import SuperService
from galeria.infrastructure.repositories.super_repository import SuperRepository
from galeria.ui.config.page_config import configurar_page
from galeria.ui.layout import RootLayout
from galeria.ui.theme.manager import ThemeManager
from galeria.ui.theme.themes import CCUEC_THEME
from galeria.ui.views import GalleryView

type FletAppTarget = Callable[[ft.Page], object | Awaitable[object]]


class FletRun(Protocol):
    def __call__(self, main: FletAppTarget, *, assets_dir: str) -> object | None: ...


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
    # Flet exposes an Unknown parameter in the published type for run().
    run_flet_app = cast(FletRun, ft.run)  # type: ignore[reportUnknownMemberType]
    run_flet_app(main, assets_dir=str(ASSETS_DIR))
