import flet as ft
from core.paths import ASSETS_DIR
from domain.models import Super


class SuperCard(ft.Container):
    def __init__(self, super_data: Super, on_click):
        super().__init__(
            content=ft.Column(
                [
                    ft.Image(
                        src=str(ASSETS_DIR / super_data.foto),
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
            ),
            padding=20,
            on_click=lambda e: on_click(super_data),
        )
