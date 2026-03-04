import flet as ft

from galeria.infrastructure.repositories.super_repository import SuperRepository
from galeria.ui.components.fade_overlay import right_fade
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.navigation_arrow import right_arrow
from galeria.ui.components.super_view import SuperDetail
from galeria.ui.controllers.GalleryScrollController import GalleryScrollController
from galeria.ui.layout.root_layout import RootLayout
from galeria.ui.theme.typography import heading_h1


class GalleryView(ft.Container):
    CARD_WIDTH = 280
    CARD_HEIGHT = 300
    VISIBLE_CARDS = 5
    SPACING = 60
    MAX_WIDTH = 1725
    PADDING = 50

    def __init__(self, page: ft.Page, root_layout: RootLayout):
        super().__init__(expand=True)

        self.root = root_layout
        self.repo = SuperRepository()

        self.supers = self.repo.listar()

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
        )

        cards_container = ft.Container(
            width=self._calculate_visible_width(),
            height=self.CARD_HEIGHT,
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        layout = ft.Column(
            [
                heading_h1(
                    "Galeria de Superintendentes",
                ),
                cards_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=60,
        )

        self.content = ft.Stack(
            [
                ft.Container(
                    content=layout,
                    width=self.MAX_WIDTH,
                    alignment=ft.Alignment.TOP_CENTER,
                    padding=self.PADDING,
                ),
                right_fade(),
                right_arrow(
                    on_click=lambda e: self.page.run_task(self.scroll_controller.next),
                ),
            ]
        )

    def _calculate_visible_width(self):
        return self.VISIBLE_CARDS * self.CARD_WIDTH + (self.VISIBLE_CARDS - 1) * self.SPACING

    def abrir_super(self, super_data):
        detail = SuperDetail(
            super_data=super_data,
            image_path=f"images/supers/{super_data.foto}",
            on_request_close=lambda: self.root.hide_overlay(detail),
        )

        self.root.show_overlay(detail)
        detail.fade_in()
