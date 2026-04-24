from typing import Any

import flet as ft

from galeria.ui.theme.manager import ThemeManager


class SuperHeader(ft.Container):
    def __init__(
        self,
        theme_manager: ThemeManager,
        image_src: str | None = None,
        nome: str = "",
        texto_inicial: str = "",
        navigation: ft.Control | None = None,
        **kwargs: Any,
    ):
        # Criação dos componentes (igual à versão funcionando)
        self.text_list = ft.ListView(
            height=433,
            spacing=12,
            controls=[],
        )
        self._set_paragraphs(texto_inicial)

        self.image = ft.Image(
            src=image_src or "images/placeholder.png",
            width=380,
            border_radius=20,
            fit=ft.BoxFit.COVER,
        )

        self.title = ft.Text(
            nome,
            size=28,
            weight=ft.FontWeight.BOLD,
        )

        self.divider = ft.Divider(thickness=3)

        text_area = ft.Column(
            expand=True,  # ← fundamental! estava faltando
            spacing=16,
            controls=[
                self.title,
                self.divider,
                self.text_list,
                navigation or ft.Container(),
            ],
        )

        layout = ft.Row(
            expand=True,
            spacing=32,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[self.image, text_area],
        )

        super().__init__(content=layout, **kwargs)

        # Integração com o ThemeManager (se fornecido)
        self._theme_manager = theme_manager
        if theme_manager:
            theme_manager.subscribe(self.on_theme_change)
            self.apply_theme(theme_manager.theme)  # usa property, não _theme

    # ========== Suporte a tema ==========
    def apply_theme(self, theme):
        """Atualiza as cores conforme o tema."""
        if theme is None:
            return
        self.divider.color = theme.primary
        self.title.color = theme.text
        for p in self.text_list.controls:
            p.color = theme.text

    def on_theme_change(self, theme):
        self.apply_theme(theme)
        self.update()

    # ========== Métodos originais ==========
    def _set_paragraphs(self, text: str):
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        self.text_list.controls = [ft.Text(p, size=14) for p in paragraphs]

    def update_text(self, new_text: str):
        self._set_paragraphs(new_text)
        if hasattr(self.text_list, "_i"):
            self.text_list.scroll_to(offset=0)
        # Reaplica o tema atual nos novos parágrafos
        if self._theme_manager:
            self.apply_theme(self._theme_manager.theme)
        self.update()
