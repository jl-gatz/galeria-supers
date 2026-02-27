import flet as ft
from domain.models import Super
from ui.components.super_card import SuperCard
from ui.events.scroll_events import criar_scroll_handler

from galeria.core.paths import ASSETS_DIR
from galeria.ui.components.super_view import SuperDetail
from galeria.ui.layout.root_layout import RootLayout


class GalleryView(ft.Container):
    def __init__(self, supers: list[Super], root_layout: RootLayout):
        self.supers = supers
        # self.navigator = navigator
        self.root = root_layout

        cards = [
            SuperCard(
                super_data=s,
                image_path=ASSETS_DIR / s.foto,
                on_open=self.abrir_super,
            )
            for s in supers
        ]

        self.galeria = ft.Row(
            controls=cards,
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )

        self.galeria.on_scroll = criar_scroll_handler(self.galeria)

        content = ft.Column(
            [
                ft.Text(
                    "Galeria dos Superintendentes",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                ),
                self.galeria,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,
        )

        super().__init__(
            content=content,
            opacity=1,
            animate_opacity=300,
            expand=True,
        )

    def fade_background(self):
        self.opacity = 0.3
        self.update()

    def restore_background(self):
        self.opacity = 1
        self.update()

    def abrir_super(self, super_data):
        detail = SuperDetail(
            super_data=super_data,
            image_path=ASSETS_DIR / super_data.foto,
            on_request_close=lambda: self._fechar_detail(detail),
        )

        self.root.show_overlay(detail)
        detail.fade_in()

        # self.fade_background()
        # self.root.show_overlay(detail)
        # detail.fade_in()

    def _fechar_detail(self, detail):
        self.root.hide_overlay(detail)
        self.restore_background()
