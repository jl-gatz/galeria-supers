# galeria/ui/views/gallery_view.py

from collections.abc import Sequence
from pathlib import Path

import flet as ft

from galeria.core import LOGO_DETIC, LOGO_UNICAMP
from galeria.domain import Super
from galeria.domain.protocols.gallery_service_like import GalleryServiceLike
from galeria.ui.components import GalleryRow, logos_row, placeholders_row, right_arrow
from galeria.ui.controllers import GalleryScrollController
from galeria.ui.layout import RootLayout
from galeria.ui.theme import h1
from galeria.ui.views.super_view import SuperDetail


class GalleryView(ft.Container):
    CARD_WIDTH = 275
    CARD_HEIGHT = 360
    VISIBLE_CARDS = 5
    SPACING = 60
    MAX_WIDTH = 1800
    PADDING = 20

    def __init__(
        self,
        page: ft.Page,
        service: GalleryServiceLike,
        root_layout: RootLayout,
        logo_detic: Path = Path(LOGO_DETIC),
        logo_unicamp: Path = Path(LOGO_UNICAMP),
        show_placeholder_left: bool = False,
        show_placeholder_right: bool = False,
    ):
        super().__init__(expand=True)

        self.root: RootLayout = root_layout
        self.service: GalleryServiceLike = service
        self.supers: Sequence[Super] = service.listar_supers()

        # Galeria rolável
        self.gallery_row = GalleryRow(
            supers=self.supers,
            card_width=self.CARD_WIDTH,
            spacing=self.SPACING,
            on_card_click=self.abrir_super,
        )

        self.scroll_controller = GalleryScrollController(
            row=self.gallery_row,
            visible_cards=self.VISIBLE_CARDS,
            card_width=self.CARD_WIDTH,
            spacing=self.SPACING,
            padding=self.PADDING,  # opcional, se o controlador precisar
        )

        # Container que envolve a galeria (sem padding extra por enquanto)
        cards_container = ft.Container(
            width=self.scroll_controller.group_width(),
            height=self.CARD_HEIGHT,
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        # Stack para sobrepor o fade
        gallery_stack = ft.Stack(
            [
                cards_container,
                # right_fade(),  # descomente se necessário
            ],
            width=self.scroll_controller.group_width() + 2 * self.PADDING,
            height=self.CARD_HEIGHT,
        )

        # Seta de navegação (abaixo da galeria)
        arrow_container = ft.Container(
            content=right_arrow(on_click=lambda _: self.page.run_task(self.scroll_controller.next)),
            alignment=ft.Alignment.CENTER,
            margin=ft.Margin.only(top=20),
        )

        # Linha com os dois logotipos (alinhados à direita)
        logos = logos_row(logo_detic, logo_unicamp)

        # Linha inferior com placeholders (um à esquerda, um à direita)
        placeholders = placeholders_row(show_placeholder_left, show_placeholder_right)

        # Layout principal (coluna)
        layout = ft.Column(
            [
                h1("Galeria de Superintendentes"),
                gallery_stack,
                arrow_container,
                logos,
                placeholders,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=self.SPACING,
        )

        # Container final que define a largura máxima e centraliza tudo
        self.content = ft.Container(
            content=layout,
            width=self.MAX_WIDTH,
            alignment=ft.Alignment.TOP_CENTER,
            padding=self.PADDING,
        )

    def abrir_super(self, super_data: Super) -> None:
        if not self.service.pode_abrir(super_data):
            return  # há um quadro "vazio" vindo do json

        detail = SuperDetail(
            super_data=super_data,
            on_request_close=lambda: self.root.hide_overlay(detail),
        )
        self.root.show_overlay(detail)
        detail.fade_in()
