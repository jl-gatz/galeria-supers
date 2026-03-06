from pathlib import Path

import flet as ft

from galeria.core.paths import LOGO_DETIC, LOGO_UNICAMP
from galeria.infrastructure.repositories.super_repository import Super
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.logos_row import logos_row
from galeria.ui.components.navigation_arrow import right_arrow
from galeria.ui.components.placeholders_row import placeholders_row
from galeria.ui.controllers.gallery_controller import GalleryController
from galeria.ui.controllers.gallery_scroll_controller import GalleryScrollController
from galeria.ui.layout.root_layout import RootLayout
from galeria.ui.theme.typography import heading_h1
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
        root_layout: RootLayout,
        logo_detic: str = LOGO_DETIC,
        logo_unicamp: str = LOGO_UNICAMP,
        show_placeholder_left: bool = False,
        show_placeholder_right: bool = False,
    ):
        super().__init__(expand=True)

        self.root = root_layout
        controller = GalleryController()

        # Galeria rolável
        self.gallery_row = GalleryRow(
            supers=controller.get_supers(),
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
            margin=ft.margin.only(top=20),
        )

        # Linha com os dois logotipos (alinhados à direita)
        logos = logos_row(logo_detic, logo_unicamp)

        # Linha inferior com placeholders (um à esquerda, um à direita)
        placeholders = placeholders_row(show_placeholder_left, show_placeholder_right)

        # Layout principal (coluna)
        layout = ft.Column(
            [
                heading_h1("Galeria de Superintendentes"),
                gallery_stack,
                arrow_container,
                logos,
                placeholders,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=60,
        )

        # Container final que define a largura máxima e centraliza tudo
        self.content = ft.Container(
            content=layout,
            width=self.MAX_WIDTH,
            alignment=ft.Alignment.TOP_CENTER,
            padding=self.PADDING,
        )

    def abrir_super(self, super_data: Super):
        if super_data.nome != "_blank":  # há um quadro "vazio" vindo do json
            detail = SuperDetail(
                super_data=super_data,
                image_path=Path(f"images/supers/{super_data.foto}"),
                on_request_close=lambda: self.root.hide_overlay(detail),
            )
            self.root.show_overlay(detail)
            detail.fade_in()
