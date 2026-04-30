from collections.abc import Callable
from typing import Any

import flet as ft

from galeria.ui.theme.styles import Theme


class GalleryRow(ft.Container):
    def __init__(
        self,
        supers: Any,
        card_width: int,
        spacing: int,
        padding: int,
        on_card_click: Callable[[], None],
        theme: Theme,
    ):
        self.supers = supers
        self.card_width = card_width
        self._theme = theme
        self._on_card_click = on_card_click

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
            height=self._theme.gallery.card_height,
            on_click=lambda e: on_card_click(super_data),
            data={"type": "card", "nome": super_data.nome},
            border_radius=self._theme.radius.md,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack(
                controls=[
                    # 📷 Imagem base
                    ft.Image(
                        src=str(super_data.foto).replace("\\", "/"),
                        fit=ft.BoxFit.COVER,
                        width=self.card_width,
                        height=self._theme.gallery.card_height,
                    ),
                    # 🎨 Overlay de tema (ESSENCIAL)
                    ft.Container(
                        bgcolor=self._theme.gallery.image_overlay,
                    ),
                    # (opcional futuro)
                    # gradiente / título / highlight
                ]
            ),
        )
