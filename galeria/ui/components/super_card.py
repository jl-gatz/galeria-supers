from collections.abc import Callable
from pathlib import Path

import flet as ft
from domain.models import Super


class SuperCard(ft.Container):
    def __init__(
        self,
        super_data: Super,
        image_path: Path,
        on_open: Callable[[Super], None],
    ):
        self._super = super_data
        self._on_open = on_open

        content = ft.Column(
            controls=[
                ft.Image(
                    src=str(image_path),
                    width=200,
                    height=200,
                    fit="cover",
                    border_radius=ft.BorderRadius.all(100),
                ),
                ft.Text(
                    super_data.nome,
                    size=20,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        super().__init__(
            content=content,
            padding=20,
            on_click=self._handle_click,
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        self._on_open(self._super)
