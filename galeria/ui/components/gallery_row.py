from typing import Any

import flet as ft


class GalleryRow(ft.Container):
    def __init__(
        self, supers: Any, card_width: int, spacing: int, padding: int, on_card_click: ft.Control
    ):
        self.supers = supers
        self.card_width = card_width

        cards = [self._build_card(s, on_card_click) for s in supers]

        self.row = ft.Row(
            controls=cards,
            spacing=spacing,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )

        super().__init__(
            content=self.row,
            padding=ft.padding.only(bottom=padding),
        )

    def _build_card(self, super_data, on_card_click):
        return ft.Container(
            width=self.card_width,
            on_click=lambda e: on_card_click(super_data),
            data={"type": "card", "nome": super_data.nome},
            content=ft.Image(
                src=str(super_data.foto).replace("\\", "/"),
                fit=ft.BoxFit.COVER,
                height=400,
            ),
        )
