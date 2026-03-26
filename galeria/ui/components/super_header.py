# ui/components/super_header.py


from typing import Any

import flet as ft

from galeria.ui.theme import PRIMARY_RED, body, h2, spacing


class SuperHeader(ft.Container):
    def __init__(self, image_src: str | None, nome: str, texto_inicial: str = "", **kwargs: Any):

        self.scroll = ft.ScrollMode.HIDDEN

        self.text_list = ft.ListView(
            # expand=True,
            height=433,
            spacing=spacing.LG,
            controls=[],
            # auto_scroll=True,
        )

        self._set_paragraphs(texto_inicial)

        image = ft.Image(
            src=image_src or "images/placeholder.png",
            width=380,
            border_radius=20,
            fit=ft.BoxFit.COVER,
        )

        text_area = ft.Column(
            expand=True,
            spacing=spacing.MD,
            controls=[
                h2(nome),
                ft.Divider(color=PRIMARY_RED, thickness=3),
                self.text_list,
            ],
        )

        layout = ft.Row(
            expand=True,
            spacing=spacing.XXL,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                image,
                text_area,
            ],
        )

        super().__init__(content=layout, **kwargs)

    def _set_paragraphs(self, text: str):
        """Divide o texto em parágrafos e atualiza a coluna rolável."""
        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        self.text_list.controls = [body(p) for p in paragraphs]

    def update_text(self, new_text: str):
        """Atualiza o conteúdo do texto exibido no header."""

        self._set_paragraphs(new_text)

        # reseta posição do scroll
        if hasattr(self.text_list, "_i"):
            self.text_list.scroll_to(offset=0)

        self.update()
