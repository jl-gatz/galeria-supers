from typing import Any

import flet as ft


class GalleryRow(ft.Row):
    def __init__(self, supers: Any, card_width: int, spacing: int, on_card_click: ft.Control):
        self.supers = supers
        self.card_width = card_width

        cards = [self._build_card(s, on_card_click) for s in supers]

        super().__init__(
            controls=cards,
            spacing=spacing,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )

    def _build_card(self, super_data, on_card_click):
        return ft.Container(
            width=self.card_width,
            on_click=lambda e: on_card_click(super_data),
            content=ft.Image(
                src=f"images/supers/{super_data.foto}",
                fit=ft.BoxFit.COVER,
                height=400,
            ),
        )
