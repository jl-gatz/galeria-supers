# galeria/ui/views/gallery_view.py

from collections.abc import Sequence
from pathlib import Path

import flet as ft

from galeria.core import LOGO_DETIC, LOGO_UNICAMP
from galeria.domain import Super
from galeria.domain.protocols import GalleryServiceLike
from galeria.ui.components import FloatingNavButton, GalleryRow, logos_row, placeholders_row
from galeria.ui.controllers import GalleryScrollController, SuperDetailController
from galeria.ui.layout import RootLayout
from galeria.ui.theme import h1
from galeria.ui.views.super_view import SuperDetail


class GalleryView(ft.Container):
    CARD_WIDTH = 300
    CARD_HEIGHT = 394
    VISIBLE_CARDS = 4
    V_SPACING = 40
    H_SPACING = 165
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

        # 🎯 Galeria rolável
        self.gallery_row = GalleryRow(
            supers=self.supers,
            card_width=self.CARD_WIDTH,
            spacing=self.H_SPACING,
            padding=self.V_SPACING,
            on_card_click=self.abrir_super,
        )

        self.scroll_controller = GalleryScrollController(
            row=self.gallery_row.row,  # A Row interna do GalleryRow
            visible_cards=self.VISIBLE_CARDS,
            card_width=self.CARD_WIDTH,
            spacing=self.H_SPACING,
            padding=self.PADDING,
        )

        # 🧩 Subcomponentes
        self.gallery_stack = self._build_gallery()
        self.logos = logos_row(logo_detic, logo_unicamp)
        self.placeholders = placeholders_row(
            show_placeholder_left,
            show_placeholder_right,
        )

        # 🧱 Layout principal
        self.content = ft.Container(
            content=self._build_main_column(),
            width=self.MAX_WIDTH,
            alignment=ft.Alignment.TOP_CENTER,
            padding=self.PADDING,
        )

    # ==========================================================
    # 🔧 BUILDERS
    # ==========================================================

    def _build_gallery(self):
        return ft.Container(
            width=self.scroll_controller.group_width(),
            height=self.gallery_height(),
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    def _build_main_column(self):
        return ft.Column(
            controls=[
                h1("Galeria de Superintendentes"),
                self._build_gallery(),
                self._build_fab(),
                self.logos,
                self.placeholders,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=self.V_SPACING,
        )

    def _build_fab(self):
        return ft.Container(
            content=FloatingNavButton.forward(
                on_click=lambda _: self.page.run_task(self.scroll_controller.next),
                key="gallery_next",
            ),
            width=self.scroll_controller.group_width() + 2 * self.PADDING,
            alignment=ft.Alignment.CENTER_RIGHT,
        )

    def gallery_height(self):
        return self.CARD_HEIGHT + self.V_SPACING

    # ==========================================================
    # 🎯 INTERAÇÕES
    # ==========================================================

    def abrir_super(self, super_data: Super) -> None:
        if not self.service.pode_abrir(super_data):
            return

        controller = SuperDetailController(super_data)

        detail = None  # placeholder

        def handle_close():
            self.root.hide_overlay(detail)

        detail = SuperDetail(
            controller=controller,
            on_request_close=handle_close,
        )

        self.root.show_overlay(detail)

        detail._fade_in()
