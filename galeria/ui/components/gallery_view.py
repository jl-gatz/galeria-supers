import flet as ft
from domain.models import Super
from ui.components.super_card import SuperCard
from ui.components.super_view import SuperDetail
from ui.events.scroll_events import criar_scroll_handler
from ui.navigation.navigator import Navigator


class GalleryView(ft.Column):
    def __init__(self, supers: list[Super], navigator: Navigator):
        self.supers = supers
        self.navigator = navigator

        cards = [SuperCard(s, self.abrir_super) for s in supers]

        self.galeria = ft.Row(
            controls=cards,
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )

        self.galeria.on_scroll = criar_scroll_handler(self.galeria)

        super().__init__(
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

    def abrir_super(self, super_data: Super):
        detail = SuperDetail(
            super_data,
            on_voltar=lambda: self.navigator.go(self),
        )
        self.navigator.go(detail)
