import flet as ft
from core.paths import ASSETS_DIR
from domain.models import Super


class SuperDetail(ft.Column):
    def __init__(self, super_data: Super, on_voltar):
        self.super_data = super_data
        self.slide_index = 0

        self.texto = ft.Text(
            super_data.historias[self.slide_index],
            size=24,
            text_align=ft.TextAlign.CENTER,
            width=800,
        )

        super().__init__(
            [
                ft.Image(
                    src=str(ASSETS_DIR / super_data.foto),
                    width=300,
                    border_radius=20,
                ),
                ft.Text(super_data.nome, size=32, weight=ft.FontWeight.BOLD),
                self.texto,
                ft.Row(
                    [
                        ft.Button("Anterior", on_click=self.anterior),
                        ft.Button("Próximo", on_click=self.proximo),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.TextButton("Voltar", on_click=lambda e: on_voltar()),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

    def proximo(self, e):
        if self.slide_index < len(self.super_data.historias) - 1:
            self.slide_index += 1
            self.texto.value = self.super_data.historias[self.slide_index]
            self.update()

    def anterior(self, e):
        if self.slide_index > 0:
            self.slide_index -= 1
            self.texto.value = self.super_data.historias[self.slide_index]
            self.update()
